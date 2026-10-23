#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO API fallback commands matching the MCP tools."""

import argparse
import sys
import uuid

from openclaw_client import OpenClawError, output, request


def parse_args():
    parser = argparse.ArgumentParser(description="SEO/GEO 检测与一键优化 API 回退工具")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("latest")
    report = sub.add_parser("report")
    report.add_argument("--report-id", type=int, required=True)
    items = sub.add_parser("optimizable")
    items.add_argument("--report-id", type=int, required=True)
    detect = sub.add_parser("start-detect")
    detect.add_argument("--confirmed", action="store_true")
    detect.add_argument("--request-id", default="")
    detect_status = sub.add_parser("detect-status")
    detect_status.add_argument("--operation-id", required=True)
    optimize = sub.add_parser("start-optimize")
    optimize.add_argument("--report-id", type=int, required=True)
    optimize.add_argument("--items", type=int, nargs="+", required=True)
    optimize.add_argument("--confirmed", action="store_true")
    optimize.add_argument("--request-id", default="")
    optimize_status = sub.add_parser("optimize-status")
    optimize_status.add_argument("--operation-id", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        if args.action == "latest":
            data = request("GET", "/seo_geo/getLatest")
        elif args.action == "report":
            data = request("GET", "/seo_geo/getReport", {"report_id": args.report_id})
        elif args.action == "optimizable":
            data = request("GET", "/seo_geo/getOptimizableItems", {"report_id": args.report_id})
        elif args.action == "start-detect":
            if not args.confirmed:
                output({
                    "need_confirm": True,
                    "message": "本次检测会消耗 Token 额度，通常需要等待几分钟。检测只生成报告，不会修改或发布网站。是否开始检测？",
                    "options": ["确认开始", "取消"],
                })
                return 3
            data = request("POST", "/seo_geo/startDetection", {
                "confirmed": True,
                "request_id": args.request_id or "legacy-detect-" + uuid.uuid4().hex,
            })
        elif args.action == "detect-status":
            data = request("GET", "/seo_geo/getDetectionStatus", {"operation_id": args.operation_id})
        elif args.action == "start-optimize":
            if not args.confirmed:
                output({
                    "need_confirm": True,
                    "message": "一键优化会修改网站后台内容，但不会自动发布公网。请先展示真实可优化项摘要，确认继续吗？",
                    "report_id": args.report_id,
                    "item_nos": args.items,
                })
                return 3
            data = request("POST", "/seo_geo/startOptimization", {
                "report_id": args.report_id,
                "item_nos": args.items,
                "confirmed": True,
                "request_id": args.request_id or "legacy-optimize-" + uuid.uuid4().hex,
            })
        else:
            data = request("GET", "/seo_geo/getOptimizationStatus", {"operation_id": args.operation_id})
        output({"action": args.action, "data": data})
        return 0
    except OpenClawError as exc:
        output({"error": str(exc), "error_code": exc.code, "data": exc.data}, ok=False)
        return 1


if __name__ == "__main__":
    sys.exit(main())
