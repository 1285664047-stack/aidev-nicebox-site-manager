# -*- coding: utf-8 -*-
"""Standard-library OpenClaw client used by API fallback scripts."""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

from config_reader import get_api_key, get_base_url


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


FULL_SITE_REQUIREMENT = """【整站生成要求】
1. 生成完整企业网站，不是单独首页。导航至少包含：首页、关于我们、产品或服务、新闻资讯、联系我们；用户已指定页面时优先采用用户清单。
2. 首页必须包含与导航对应的栏目内容，使系统能够提取并创建内页；导航和内容须使用 Nicebox 规定的 data-type 结构。
3. 产品或服务栏目生成 6-8 条与业务一致的示例内容；新闻资讯栏目生成 6-8 条相关文章。
4. 不得虚构价格、认证、客户案例、联系方式或功效；不确定的信息使用中性描述。
5. 必须生成普通内页、产品/新闻列表和对应详情页，而不只是首页。"""


def complete_site_requirement(requirement):
    requirement = (requirement or "").strip()
    if "【整站生成要求】" in requirement:
        return requirement
    return requirement + "\n\n" + FULL_SITE_REQUIREMENT


class OpenClawError(RuntimeError):
    def __init__(self, message, code="API_ERROR", data=None):
        super().__init__(message)
        self.code = code
        self.data = data


def request(method, path, payload=None, timeout=60):
    api_key = get_api_key()
    if not api_key:
        raise OpenClawError("API 密钥未配置，请先运行 set-key.py", "API_KEY_MISSING")
    url = get_base_url().rstrip("/") + path
    data = None
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "User-Agent": "nicebox-site-manager/2.0",
    }
    if method.upper() == "GET" and payload:
        url += "?" + urllib.parse.urlencode(payload)
    elif payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise OpenClawError("无法连接 Nicebox API：%s" % exc, "DEPENDENCY_UNAVAILABLE") from exc
    try:
        envelope = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise OpenClawError("Nicebox API 返回的不是有效 JSON", "INVALID_RESPONSE") from exc
    if int(envelope.get("code", 500)) not in (0, 200):
        details = envelope.get("data") or {}
        code = details.get("error_code", "API_ERROR") if isinstance(details, dict) else "API_ERROR"
        raise OpenClawError(envelope.get("message") or "Nicebox API 请求失败", code, details)
    return envelope.get("data")


def output(data, ok=True):
    print(json.dumps({"ok": ok, **data}, ensure_ascii=False, indent=2))
