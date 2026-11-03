#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail when an MCP tool has no checked-in ordinary API fallback."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS_FILE = ROOT / "mcp-server" / "src" / "tools.ts"
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
MANIFEST_FILE = SCRIPT_DIR / "fallback_manifest.json"
API_TOOL_FILE = SCRIPT_DIR / "api_tool.py"
PROMPT_SYNC_SCRIPT = SCRIPT_DIR / "sync_page_prompt_library.py"

PAGE_TOOLS = {
    "nicebox_list_pages": "listPages",
    "nicebox_get_page_metadata": "getPageMetadata",
    "nicebox_get_page_sections": "getPageSections",
    "nicebox_get_page_code": "getPageCode",
    "nicebox_get_page_width_settings": "getPageWidthSettings",
    "nicebox_diagnose_page_components": "diagnosePageComponents",
    "nicebox_validate_page_change": "validatePageChange",
    "nicebox_preview_page_width_settings": "previewPageWidthSettings",
    "nicebox_create_page_preview": "createPagePreview",
    "nicebox_create_page_width_preview": "createPageWidthPreview",
    "nicebox_get_page_preview": "getPagePreview",
    "nicebox_abandon_page_preview": "abandonPagePreview",
    "nicebox_commit_page_change": "commitPageChange",
    "nicebox_commit_page_width_settings": "commitPageWidthSettings",
    "nicebox_get_page_change_operation": "getPageChangeOperation",
    "nicebox_list_page_backups": "listPageBackups",
    "nicebox_preview_page_backup": "previewPageBackup",
    "nicebox_commit_page_backup": "commitPageBackup",
}

LEGACY_PAGE_FLOW_FILES = [
    ROOT / "nicebox-site-manager-main" / "skills" / "page_code_read.skill.md",
    ROOT / "nicebox-site-manager-main" / "skills" / "page_code_validate.skill.md",
    ROOT / "nicebox-site-manager-main" / "skills" / "page_change_workflow.skill.md",
    ROOT / "nicebox-site-manager-main" / "skills" / "page_dynamic_components.skill.md",
]

WORKBUDDY_PAGE_FLOW_FILES = [
    ROOT / "workbuddy-connector" / "skills" / "nicebox-site-manager" / "references" / "页面代码读取流程.md",
    ROOT / "workbuddy-connector" / "skills" / "nicebox-site-manager" / "references" / "页面修改草稿与校验流程.md",
    ROOT / "workbuddy-connector" / "skills" / "nicebox-site-manager" / "references" / "页面预览保存与回退流程.md",
    ROOT / "workbuddy-connector" / "skills" / "nicebox-site-manager" / "references" / "动态组件与复杂页面流程.md",
]

def joined_text(files):
    return "\n".join(path.read_text(encoding="utf-8") for path in files)

def main():
    source = TOOLS_FILE.read_text(encoding="utf-8")
    tools = set(re.findall(r"(?:registerApiTool\(|registerTool\()\s*(?:server,\s*client,\s*)?['\"](nicebox_[a-z0-9_]+)['\"]", source))
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    missing = sorted(tools - set(manifest))
    stale = sorted(set(manifest) - tools)
    missing_scripts = []
    for tool, command in manifest.items():
        script = command.split()[0]
        if script.endswith((".py", ".mjs")) and not (SCRIPT_DIR / script).is_file():
            missing_scripts.append("%s -> %s" % (tool, script))
    api_tool_source = API_TOOL_FILE.read_text(encoding="utf-8")
    controller_source = (ROOT / "api" / "app" / "openclaw" / "controller" / "SitePages.php").read_text(encoding="utf-8")
    legacy_flow = joined_text(LEGACY_PAGE_FLOW_FILES)
    workbuddy_flow = joined_text(WORKBUDDY_PAGE_FLOW_FILES)
    page_contract_errors = []
    for tool, controller_method in PAGE_TOOLS.items():
        checks = {
            "mcp": tool in tools,
            "fallback_manifest": tool in manifest,
            "ordinary_api_script": ('"%s"' % tool) in api_tool_source,
            "ordinary_api_controller": ("function %s(" % controller_method) in controller_source,
            "legacy_skill": tool in legacy_flow,
            "workbuddy_skill": tool in workbuddy_flow,
        }
        absent = [name for name, present in checks.items() if not present]
        if absent:
            page_contract_errors.append({"tool": tool, "missing": absent})

    prompt_library_errors = []
    canonical_prompt_dir = ROOT / "doc" / "workbuddy" / "页面修改能力" / "page-edit-prompts"
    prompt_manifest_file = canonical_prompt_dir / "manifest.json"
    prompt_manifest = {}
    if not PROMPT_SYNC_SCRIPT.is_file() or not prompt_manifest_file.is_file():
        prompt_library_errors.append("canonical prompt library or synchronization script is missing")
    else:
        prompt_manifest = json.loads(prompt_manifest_file.read_text(encoding="utf-8"))
        prompt_files = ["manifest.json", *prompt_manifest.get("files", [])]
        prompt_targets = [
            ROOT / "nicebox-site-manager-main" / "references" / "page-edit-library",
            ROOT / "workbuddy-connector" / "skills" / "nicebox-site-manager" / "references" / "page-edit-library",
        ]
        for relative in prompt_files:
            source_file = canonical_prompt_dir / relative
            if not source_file.is_file():
                prompt_library_errors.append("missing canonical prompt file: %s" % relative)
                continue
            source_content = source_file.read_bytes()
            for target in prompt_targets:
                target_file = target / relative
                if not target_file.is_file() or target_file.read_bytes() != source_content:
                    prompt_library_errors.append("prompt library out of sync: %s" % target_file)

    if missing or stale or missing_scripts or page_contract_errors or prompt_library_errors:
        print(json.dumps({"ok": False, "mcp_tool_count": len(tools), "fallback_count": len(manifest), "missing": missing, "stale": stale, "missing_scripts": missing_scripts, "page_contract_errors": page_contract_errors, "prompt_library_errors": prompt_library_errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "mcp_tool_count": len(tools), "fallback_count": len(manifest), "page_tool_count": len(PAGE_TOOLS), "prompt_library_version": prompt_manifest["library_version"], "message": "所有 MCP 工具均已登记普通 API 回退，页面修改工具与提示词库已同步到普通 API 和两个 Skill"}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": sys.exit(main())
