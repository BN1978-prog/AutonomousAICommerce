# Core Autopilot Architecture

Created at: 2026-06-29T20:30:52.318642+00:00
Steps: 71

## 1. Tokens and channel health

### 2. `token_manager`
- Command: `python -m app.token_manager`
- File: `app/token_manager.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/token_manager_status.json`
- ENV:
  - `EBAY_CLIENT_ID`
  - `EBAY_CLIENT_SECRET`
  - `EBAY_REFRESH_TOKEN`
  - `GOOGLE_ADS_CLIENT_ID`
  - `GOOGLE_ADS_CLIENT_SECRET`
  - `GOOGLE_ADS_REFRESH_TOKEN`
  - `META_ACCESS_TOKEN`
  - `META_APP_ID`
  - `META_APP_SECRET`
  - `SHOPIFY_ACCESS_TOKEN`
  - `SHOPIFY_ADMIN_ACCESS_TOKEN`
  - `SHOPIFY_ADMIN_TOKEN`

### 3. `refresh_ebay_token`
- Command: `python -m app.refresh_ebay_token`
- File: `app/refresh_ebay_token.py`
- Exists: `True`
- ENV:
  - `EBAY_CLIENT_ID`
  - `EBAY_CLIENT_SECRET`
  - `EBAY_REFRESH_TOKEN`

### 4. `google_ads_token_refresher`
- Command: `python -m app.google_ads_token_refresher`
- File: `app/google_ads_token_refresher.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_ads_token_refresher.json`
- ENV:
  - `GOOGLE_ADS_CLIENT_ID`
  - `GOOGLE_ADS_CLIENT_SECRET`
  - `GOOGLE_ADS_REFRESH_TOKEN`

### 5. `meta_token_refresh`
- Command: `python -m app.meta_token_refresh`
- File: `app/meta_token_refresh.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/meta_token_refresh.json`

### 6. `meta_page_token_refresh`
- Command: `python -m app.meta_page_token_refresh`
- File: `app/meta_page_token_refresh.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/meta_page_token_refresh.json`
- ENV:
  - `META_ACCESS_TOKEN`
  - `META_PAGE_ID`

### 7. `amazon_token_refresher`
- Command: `python -m app.amazon_token_refresher`
- File: `app/amazon_token_refresher.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/amazon_token_refresher.json`
- ENV:
  - `AMAZON_LWA_CLIENT_ID`
  - `AMAZON_LWA_CLIENT_SECRET`
  - `AMAZON_REFRESH_TOKEN`

### 13. `etsy_connection_status`
- Command: `python -m app.etsy_connection_status`
- File: `app/etsy_connection_status.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/etsy_connection_status.json`

### 33. `system_status_report`
- Command: `python -m app.system_status_report`
- File: `app/system_status_report.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/action_executor.json`
  - `app/logs/amazon_connection_status.json`
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/autopilot_run.json`
  - `app/logs/crm_readiness_summary.json`
  - `app/logs/etsy_autopilot.json`
  - `app/logs/etsy_connection_status.json`
  - `app/logs/google_campaign_live_creator.json`
  - `app/logs/master_system_health.json`
  - `app/logs/meta_launch_readiness.json`

### 53. `meta_long_lived_token`
- Command: `python -m app.meta_long_lived_token`
- File: `app/meta_long_lived_token.py`
- Exists: `False`

### 61. `customer_fulfillment_support_status`
- Command: `python -m app.customer_fulfillment_support_status`
- File: `app/customer_fulfillment_support_status.py`
- Exists: `False`

### 64. `refresh_shopify_token`
- Command: `python -m app.refresh_shopify_token`
- File: `app/refresh_shopify_token.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/shopify_token_refresh.json`

### 71. `autonomous_fulfillment_status`
- Command: `python -m app.autonomous_fulfillment_status`
- File: `app/autonomous_fulfillment_status.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/autonomous_fulfillment_status.json`
  - `app/logs/autonomy_limits.json`
  - `app/logs/supplier_purchase_queue.json`


## 2. Sales and CRM

### 8. `shopify_crm_events`
- Command: `python -m app.shopify_crm_events`
- File: `app/shopify_crm_events.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/shopify_crm_events.json`
- ENV:
  - `SHOPIFY_ACCESS_TOKEN`
  - `SHOPIFY_ADMIN_TOKEN`
  - `SHOPIFY_API_VERSION`
  - `SHOPIFY_SHOP_DOMAIN`
  - `SHOPIFY_STORE_URL`

### 9. `real_sales_collector`
- Command: `python -m app.real_sales_collector`
- File: `app/real_sales_collector.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/imported_skus.json`
  - `app/logs/real_sales_report.json`
- ENV:
  - `EBAY_ACCESS_TOKEN`
  - `EBAY_API_BASE`
  - `EBAY_OAUTH_TOKEN`
  - `EBAY_USER_TOKEN`
  - `SHOPIFY_ACCESS_TOKEN`
  - `SHOPIFY_ADMIN_TOKEN`
  - `SHOPIFY_API_VERSION`
  - `SHOPIFY_STORE_URL`
  - `WC_CONSUMER_KEY`
  - `WC_CONSUMER_SECRET`
  - `WC_STORE_URL`
  - `WOOCOMMERCE_CONSUMER_KEY`

### 11. `crm_personalized_drafts`
- Command: `python -m app.crm_personalized_drafts`
- File: `app/crm_personalized_drafts.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/crm_personalized_drafts.json`
  - `app/logs/shopify_crm_events.json`

### 12. `crm_readiness_summary`
- Command: `python -m app.crm_readiness_summary`
- File: `app/crm_readiness_summary.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/crm_channel_readiness.json`
  - `app/logs/crm_health_check.json`
  - `app/logs/crm_queue.json`
  - `app/logs/crm_readiness_summary.json`
  - `app/logs/crm_send_guard.json`
  - `app/logs/smtp_config_validator.json`


## 3. Product discovery and planning

### 17. `exploration_engine_v2`
- Command: `python -m app.exploration_engine_v2`
- File: `app/exploration_engine_v2.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/exploration_v2.json`
  - `app/logs/product_performance.json`

### 18. `build_priority_queue`
- Command: `python -m app.build_priority_queue`
- File: `app/build_priority_queue.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/exploration_v2.json`
  - `app/logs/product_performance.json`

### 19. `publish_execution_plan`
- Command: `python -m app.publish_execution_plan`
- File: `app/publish_execution_plan.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/publish_execution_plan.json`

### 36. `product_guardrails`
- Command: `python -m app.product_guardrails`
- File: `app/product_guardrails.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/product_guardrails.json`

### 66. `listing_publish_execution_plan_real`
- Command: `python -m app.listing_publish_execution_plan_real`
- File: `app/listing_publish_execution_plan_real.py`
- Exists: `False`


## 4. Content and campaigns

### 26. `social_content_generator`
- Command: `python -m app.social_content_generator`
- File: `app/social_content_generator.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/publish_execution_plan.json`
  - `app/logs/social_content_plan.json`

### 27. `social_content_enhancer`
- Command: `python -m app.social_content_enhancer`
- File: `app/social_content_enhancer.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/social_content_enhanced.json`
  - `app/logs/social_content_plan.json`

### 29. `meta_ad_drafts_from_content`
- Command: `python -m app.meta_ad_drafts_from_content`
- File: `app/meta_ad_drafts_from_content.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/meta_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 30. `google_ad_drafts_from_content`
- Command: `python -m app.google_ad_drafts_from_content`
- File: `app/google_ad_drafts_from_content.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 31. `campaign_hub`
- Command: `python -m app.campaign_hub`
- File: `app/campaign_hub.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/campaign_hub.json`
  - `app/logs/google_ad_drafts_from_content.json`
  - `app/logs/meta_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 32. `campaign_approval_queue`
- Command: `python -m app.campaign_approval_queue`
- File: `app/campaign_approval_queue.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/campaign_approval_queue.json`
  - `app/logs/campaign_hub.json`

### 47. `meta_live_campaign_builder`
- Command: `python -m app.meta_live_campaign_builder`
- File: `app/meta_live_campaign_builder.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_backend_router.json`
  - `app/logs/meta_live_campaign_payloads.json`

### 48. `google_live_campaign_builder`
- Command: `python -m app.google_live_campaign_builder`
- File: `app/google_live_campaign_builder.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_backend_router.json`

### 49. `live_campaign_registry`
- Command: `python -m app.live_campaign_registry`
- File: `app/live_campaign_registry.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_campaign_registry.json`
  - `app/logs/meta_live_campaign_payloads.json`


## 5. Publishing guard and reports

### 12. `crm_readiness_summary`
- Command: `python -m app.crm_readiness_summary`
- File: `app/crm_readiness_summary.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/crm_channel_readiness.json`
  - `app/logs/crm_health_check.json`
  - `app/logs/crm_queue.json`
  - `app/logs/crm_readiness_summary.json`
  - `app/logs/crm_send_guard.json`
  - `app/logs/smtp_config_validator.json`

### 33. `system_status_report`
- Command: `python -m app.system_status_report`
- File: `app/system_status_report.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/action_executor.json`
  - `app/logs/amazon_connection_status.json`
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/autopilot_run.json`
  - `app/logs/crm_readiness_summary.json`
  - `app/logs/etsy_autopilot.json`
  - `app/logs/etsy_connection_status.json`
  - `app/logs/google_campaign_live_creator.json`
  - `app/logs/master_system_health.json`
  - `app/logs/meta_launch_readiness.json`

### 34. `daily_summary`
- Command: `python -m app.daily_summary`
- File: `app/daily_summary.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/autopilot_run.json`
  - `app/logs/product_performance.json`

### 38. `ceo_dashboard`
- Command: `python -m app.ceo_dashboard`
- File: `app/ceo_dashboard.py`
- Exists: `True`

### 59. `send_daily_summary`
- Command: `python -m app.send_daily_summary`
- File: `app/send_daily_summary.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/send_daily_summary.json`
- ENV:
  - `OWNER_EMAIL`
  - `SMTP_FROM_EMAIL`
  - `SMTP_HOST`
  - `SMTP_PASSWORD`
  - `SMTP_PORT`
  - `SMTP_USER`

### 60. `send_telegram_summary`
- Command: `python -m app.send_telegram_summary`
- File: `app/send_telegram_summary.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/send_telegram_summary.json`
- ENV:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`


## 6. Scaling and ROI safety

### 35. `auto_scaling_score`
- Command: `python -m app.auto_scaling_score`
- File: `app/auto_scaling_score.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_scaling_score.json`

### 37. `roi_simulation`
- Command: `python -m app.roi_simulation`
- File: `app/roi_simulation.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_scaling_score.json`
  - `app/logs/roi_simulation.json`

### 40. `auto_spend_executor`
- Command: `python -m app.auto_spend_executor`
- File: `app/auto_spend_executor.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_launch_decisions.json`
  - `app/logs/auto_spend_executor.json`

### 41. `spend_history_tracker`
- Command: `python -m app.spend_history_tracker`
- File: `app/spend_history_tracker.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/spend_history_tracker.json`

### 42. `negative_roi_auto_pause`
- Command: `python -m app.negative_roi_auto_pause`
- File: `app/negative_roi_auto_pause.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/negative_roi_auto_pause.json`
  - `app/logs/spend_history_tracker.json`

### 43. `hourly_budget_monitor`
- Command: `python -m app.hourly_budget_monitor`
- File: `app/hourly_budget_monitor.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/hourly_budget_monitor.json`

### 44. `emergency_stop_validator`
- Command: `python -m app.emergency_stop_validator`
- File: `app/emergency_stop_validator.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/emergency_stop_validator.json`
  - `app/logs/hourly_budget_monitor.json`

### 45. `live_spend_permission_gate`
- Command: `python -m app.live_spend_permission_gate`
- File: `app/live_spend_permission_gate.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/emergency_stop_validator.json`
  - `app/logs/live_spend_permission_gate.json`

### 57. `live_spend_audit_ledger`
- Command: `python -m app.live_spend_audit_ledger`
- File: `app/live_spend_audit_ledger.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_execution_consolidated.json`
  - `app/logs/live_spend_audit_ledger.jsonl`

### 58. `live_spend_audit_reader`
- Command: `python -m app.live_spend_audit_reader`
- File: `app/live_spend_audit_reader.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_spend_audit_ledger.jsonl`


## 7. Live ads execution

### 45. `live_spend_permission_gate`
- Command: `python -m app.live_spend_permission_gate`
- File: `app/live_spend_permission_gate.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/emergency_stop_validator.json`
  - `app/logs/live_spend_permission_gate.json`

### 46. `live_backend_router`
- Command: `python -m app.live_backend_router`
- File: `app/live_backend_router.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_backend_router.json`
  - `app/logs/live_spend_permission_gate.json`

### 47. `meta_live_campaign_builder`
- Command: `python -m app.meta_live_campaign_builder`
- File: `app/meta_live_campaign_builder.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_backend_router.json`
  - `app/logs/meta_live_campaign_payloads.json`

### 48. `google_live_campaign_builder`
- Command: `python -m app.google_live_campaign_builder`
- File: `app/google_live_campaign_builder.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_backend_router.json`

### 49. `live_campaign_registry`
- Command: `python -m app.live_campaign_registry`
- File: `app/live_campaign_registry.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_campaign_registry.json`
  - `app/logs/meta_live_campaign_payloads.json`

### 50. `live_api_execution_gate`
- Command: `python -m app.live_api_execution_gate`
- File: `app/live_api_execution_gate.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_api_execution_gate.json`
  - `app/logs/live_campaign_registry.json`
  - `app/logs/live_spend_permission_gate.json`

### 51. `live_execution_reporter`
- Command: `python -m app.live_execution_reporter`
- File: `app/live_execution_reporter.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_api_execution_gate.json`
  - `app/logs/live_execution_report.json`

### 52. `live_mode_final_lock`
- Command: `python -m app.live_mode_final_lock`
- File: `app/live_mode_final_lock.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_execution_report.json`
  - `app/logs/live_mode_final_lock.json`

### 53. `meta_long_lived_token`
- Command: `python -m app.meta_long_lived_token`
- File: `app/meta_long_lived_token.py`
- Exists: `False`

### 54. `meta_live_executor`
- Command: `python -m app.meta_live_executor`
- File: `app/meta_live_executor.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_mode_final_lock.json`
  - `app/logs/meta_live_campaign_payloads.json`
  - `app/logs/meta_live_execution_result.json`
- ENV:
  - `META_ACCESS_TOKEN`
  - `META_AD_ACCOUNT_ID`
  - `META_API_VERSION`

### 55. `google_live_executor`
- Command: `python -m app.google_live_executor`
- File: `app/google_live_executor.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/google_live_execution_result.json`
  - `app/logs/live_mode_final_lock.json`

### 56. `live_execution_consolidator`
- Command: `python -m app.live_execution_consolidator`
- File: `app/live_execution_consolidator.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/google_live_execution_result.json`
  - `app/logs/live_execution_consolidated.json`
  - `app/logs/meta_live_execution_result.json`

### 57. `live_spend_audit_ledger`
- Command: `python -m app.live_spend_audit_ledger`
- File: `app/live_spend_audit_ledger.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_execution_consolidated.json`
  - `app/logs/live_spend_audit_ledger.jsonl`

### 58. `live_spend_audit_reader`
- Command: `python -m app.live_spend_audit_reader`
- File: `app/live_spend_audit_reader.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/live_spend_audit_ledger.jsonl`


## 8. Fulfillment / suppliers

### 10. `cj_paid_order_fulfillment`
- Command: `python -m app.cj_paid_order_fulfillment`
- File: `app/cj_paid_order_fulfillment.py`
- Exists: `False`

### 13. `etsy_connection_status`
- Command: `python -m app.etsy_connection_status`
- File: `app/etsy_connection_status.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/etsy_connection_status.json`

### 14. `etsy_autopilot`
- Command: `python -m app.etsy_autopilot`
- File: `app/etsy_autopilot.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/etsy_autopilot.json`
- ENV:
  - `ETSY_ACCESS_TOKEN`

### 21. `cj_trend_bridge`
- Command: `python -m app.cj_trend_bridge`
- File: `app/cj_trend_bridge.py`
- Exists: `False`

### 22. `supplier_candidate_filter`
- Command: `python app/filter_supplier_candidates.py`
- File: `app/filter_supplier_candidates.py`
- Exists: `False`

### 61. `customer_fulfillment_support_status`
- Command: `python -m app.customer_fulfillment_support_status`
- File: `app/customer_fulfillment_support_status.py`
- Exists: `False`

### 71. `autonomous_fulfillment_status`
- Command: `python -m app.autonomous_fulfillment_status`
- File: `app/autonomous_fulfillment_status.py`
- Exists: `True`
- Reads/Writes logs mentioned:
  - `app/logs/autonomous_fulfillment_status.json`
  - `app/logs/autonomy_limits.json`
  - `app/logs/supplier_purchase_queue.json`


## Full ordered chain

1. `railway_health_check` ? `app/railway_health_check.py` exists=False
2. `token_manager` ? `app/token_manager.py` exists=True
3. `refresh_ebay_token` ? `app/refresh_ebay_token.py` exists=True
4. `google_ads_token_refresher` ? `app/google_ads_token_refresher.py` exists=True
5. `meta_token_refresh` ? `app/meta_token_refresh.py` exists=True
6. `meta_page_token_refresh` ? `app/meta_page_token_refresh.py` exists=True
7. `amazon_token_refresher` ? `app/amazon_token_refresher.py` exists=True
8. `shopify_crm_events` ? `app/shopify_crm_events.py` exists=True
9. `real_sales_collector` ? `app/real_sales_collector.py` exists=True
10. `cj_paid_order_fulfillment` ? `app/cj_paid_order_fulfillment.py` exists=False
11. `crm_personalized_drafts` ? `app/crm_personalized_drafts.py` exists=True
12. `crm_readiness_summary` ? `app/crm_readiness_summary.py` exists=True
13. `etsy_connection_status` ? `app/etsy_connection_status.py` exists=True
14. `etsy_autopilot` ? `app/etsy_autopilot.py` exists=True
15. `real_trend_discovery` ? `app/real_trend_discovery.py` exists=False
16. `autonomous_trend_filter` ? `app/autonomous_trend_filter.py` exists=False
17. `exploration_engine_v2` ? `app/exploration_engine_v2.py` exists=True
18. `build_priority_queue` ? `app/build_priority_queue.py` exists=True
19. `publish_execution_plan` ? `app/publish_execution_plan.py` exists=True
20. `trend_listing_validator` ? `app/trend_listing_validator.py` exists=False
21. `cj_trend_bridge` ? `app/cj_trend_bridge.py` exists=False
22. `supplier_candidate_filter` ? `app/filter_supplier_candidates.py` exists=False
23. `seo_product_optimizer` ? `app/seo_product_optimizer.py` exists=False
24. `profit_checked_products` ? `app/profit_checked_products.py` exists=False
25. `action_executor` ? `app/action_executor.py` exists=True
26. `social_content_generator` ? `app/social_content_generator.py` exists=True
27. `social_content_enhancer` ? `app/social_content_enhancer.py` exists=True
28. `auto_publish_or_fallback` ? `app/auto_publish_or_fallback.py` exists=True
29. `meta_ad_drafts_from_content` ? `app/meta_ad_drafts_from_content.py` exists=True
30. `google_ad_drafts_from_content` ? `app/google_ad_drafts_from_content.py` exists=True
31. `campaign_hub` ? `app/campaign_hub.py` exists=True
32. `campaign_approval_queue` ? `app/campaign_approval_queue.py` exists=True
33. `system_status_report` ? `app/system_status_report.py` exists=True
34. `daily_summary` ? `app/daily_summary.py` exists=True
35. `auto_scaling_score` ? `app/auto_scaling_score.py` exists=True
36. `product_guardrails` ? `app/product_guardrails.py` exists=True
37. `roi_simulation` ? `app/roi_simulation.py` exists=True
38. `ceo_dashboard` ? `app/ceo_dashboard.py` exists=True
39. `auto_launch_engine` ? `app/auto_launch_engine.py` exists=True
40. `auto_spend_executor` ? `app/auto_spend_executor.py` exists=True
41. `spend_history_tracker` ? `app/spend_history_tracker.py` exists=True
42. `negative_roi_auto_pause` ? `app/negative_roi_auto_pause.py` exists=True
43. `hourly_budget_monitor` ? `app/hourly_budget_monitor.py` exists=True
44. `emergency_stop_validator` ? `app/emergency_stop_validator.py` exists=True
45. `live_spend_permission_gate` ? `app/live_spend_permission_gate.py` exists=True
46. `live_backend_router` ? `app/live_backend_router.py` exists=True
47. `meta_live_campaign_builder` ? `app/meta_live_campaign_builder.py` exists=True
48. `google_live_campaign_builder` ? `app/google_live_campaign_builder.py` exists=True
49. `live_campaign_registry` ? `app/live_campaign_registry.py` exists=True
50. `live_api_execution_gate` ? `app/live_api_execution_gate.py` exists=True
51. `live_execution_reporter` ? `app/live_execution_reporter.py` exists=True
52. `live_mode_final_lock` ? `app/live_mode_final_lock.py` exists=True
53. `meta_long_lived_token` ? `app/meta_long_lived_token.py` exists=False
54. `meta_live_executor` ? `app/meta_live_executor.py` exists=True
55. `google_live_executor` ? `app/google_live_executor.py` exists=True
56. `live_execution_consolidator` ? `app/live_execution_consolidator.py` exists=True
57. `live_spend_audit_ledger` ? `app/live_spend_audit_ledger.py` exists=True
58. `live_spend_audit_reader` ? `app/live_spend_audit_reader.py` exists=True
59. `send_daily_summary` ? `app/send_daily_summary.py` exists=True
60. `send_telegram_summary` ? `app/send_telegram_summary.py` exists=True
61. `customer_fulfillment_support_status` ? `app/customer_fulfillment_support_status.py` exists=False
62. `env_backup_sync` ? `None` exists=False
63. `env_channel_recovery` ? `app/env_channel_recovery.py` exists=False
64. `refresh_shopify_token` ? `app/refresh_shopify_token.py` exists=True
65. `railway_env_sync` ? `app/railway_env_sync.py` exists=False
66. `listing_publish_execution_plan_real` ? `app/listing_publish_execution_plan_real.py` exists=False
67. `marketplace_listing_publisher` ? `app/marketplace_listing_publisher.py` exists=False
68. `draft_listing_activation_plan` ? `app/draft_listing_activation_plan.py` exists=False
69. `draft_listing_activator` ? `app/draft_listing_activator.py` exists=False
70. `marketplace_order_autobuy` ? `app/marketplace_order_autobuy.py` exists=False
71. `autonomous_fulfillment_status` ? `app/autonomous_fulfillment_status.py` exists=True