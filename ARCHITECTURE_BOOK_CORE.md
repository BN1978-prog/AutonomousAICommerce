# AICommerce Core Architecture Book

Created at: 2026-06-29T20:36:55.379055+00:00

## Summary

- Total autopilot steps: 71
- Existing modules: 52
- Missing modules: 19

## Full Autopilot Flow

### 1. railway_health_check
- Status: MISSING
- Command: `python -m app.railway_health_check`
- File: `app/railway_health_check.py`

### 2. token_manager
- Status: OK
- Command: `python -m app.token_manager`
- File: `app/token_manager.py`
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
  - `SHOPIFY_API_VERSION`
  - `SHOPIFY_SHOP`
  - `SHOPIFY_STORE_URL`
  - `WC_CONSUMER_KEY`
  - `WC_CONSUMER_SECRET`
  - `WC_STORE_URL`
  - `WOOCOMMERCE_CONSUMER_KEY`
  - `WOOCOMMERCE_CONSUMER_SECRET`
  - `WOOCOMMERCE_STORE_URL`
  - `WOO_CONSUMER_KEY`
  - `WOO_CONSUMER_SECRET`
  - `WOO_STORE_URL`
- Logs:
  - `app/logs/token_manager_status.json`

### 3. refresh_ebay_token
- Status: OK
- Command: `python -m app.refresh_ebay_token`
- File: `app/refresh_ebay_token.py`
- ENV:
  - `EBAY_CLIENT_ID`
  - `EBAY_CLIENT_SECRET`
  - `EBAY_REFRESH_TOKEN`

### 4. google_ads_token_refresher
- Status: OK
- Command: `python -m app.google_ads_token_refresher`
- File: `app/google_ads_token_refresher.py`
- ENV:
  - `GOOGLE_ADS_CLIENT_ID`
  - `GOOGLE_ADS_CLIENT_SECRET`
  - `GOOGLE_ADS_REFRESH_TOKEN`
- Logs:
  - `app/logs/google_ads_token_refresher.json`

### 5. meta_token_refresh
- Status: OK
- Command: `python -m app.meta_token_refresh`
- File: `app/meta_token_refresh.py`
- Logs:
  - `app/logs/meta_token_refresh.json`

### 6. meta_page_token_refresh
- Status: OK
- Command: `python -m app.meta_page_token_refresh`
- File: `app/meta_page_token_refresh.py`
- ENV:
  - `META_ACCESS_TOKEN`
  - `META_PAGE_ID`
- Logs:
  - `app/logs/meta_page_token_refresh.json`

### 7. amazon_token_refresher
- Status: OK
- Command: `python -m app.amazon_token_refresher`
- File: `app/amazon_token_refresher.py`
- ENV:
  - `AMAZON_LWA_CLIENT_ID`
  - `AMAZON_LWA_CLIENT_SECRET`
  - `AMAZON_REFRESH_TOKEN`
- Logs:
  - `app/logs/amazon_token_refresher.json`

### 8. shopify_crm_events
- Status: OK
- Command: `python -m app.shopify_crm_events`
- File: `app/shopify_crm_events.py`
- ENV:
  - `SHOPIFY_ACCESS_TOKEN`
  - `SHOPIFY_ADMIN_TOKEN`
  - `SHOPIFY_API_VERSION`
  - `SHOPIFY_SHOP_DOMAIN`
  - `SHOPIFY_STORE_URL`
- Logs:
  - `app/logs/shopify_crm_events.json`

### 9. real_sales_collector
- Status: OK
- Command: `python -m app.real_sales_collector`
- File: `app/real_sales_collector.py`
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
  - `WOOCOMMERCE_CONSUMER_SECRET`
  - `WOOCOMMERCE_STORE_URL`
  - `WOO_CONSUMER_KEY`
  - `WOO_CONSUMER_SECRET`
  - `WOO_STORE_URL`
- Logs:
  - `app/logs/imported_skus.json`
  - `app/logs/real_sales_report.json`

### 10. cj_paid_order_fulfillment
- Status: MISSING
- Command: `python -m app.cj_paid_order_fulfillment`
- File: `app/cj_paid_order_fulfillment.py`

### 11. crm_personalized_drafts
- Status: OK
- Command: `python -m app.crm_personalized_drafts`
- File: `app/crm_personalized_drafts.py`
- Logs:
  - `app/logs/crm_personalized_drafts.json`
  - `app/logs/shopify_crm_events.json`

### 12. crm_readiness_summary
- Status: OK
- Command: `python -m app.crm_readiness_summary`
- File: `app/crm_readiness_summary.py`
- Logs:
  - `app/logs/crm_channel_readiness.json`
  - `app/logs/crm_health_check.json`
  - `app/logs/crm_queue.json`
  - `app/logs/crm_readiness_summary.json`
  - `app/logs/crm_send_guard.json`
  - `app/logs/smtp_config_validator.json`

### 13. etsy_connection_status
- Status: OK
- Command: `python -m app.etsy_connection_status`
- File: `app/etsy_connection_status.py`
- Logs:
  - `app/logs/etsy_connection_status.json`

### 14. etsy_autopilot
- Status: OK
- Command: `python -m app.etsy_autopilot`
- File: `app/etsy_autopilot.py`
- ENV:
  - `ETSY_ACCESS_TOKEN`
- Logs:
  - `app/logs/etsy_autopilot.json`

### 15. real_trend_discovery
- Status: MISSING
- Command: `python -m app.real_trend_discovery`
- File: `app/real_trend_discovery.py`

### 16. autonomous_trend_filter
- Status: MISSING
- Command: `python -m app.autonomous_trend_filter`
- File: `app/autonomous_trend_filter.py`

### 17. exploration_engine_v2
- Status: OK
- Command: `python -m app.exploration_engine_v2`
- File: `app/exploration_engine_v2.py`
- Logs:
  - `app/logs/exploration_v2.json`
  - `app/logs/product_performance.json`

### 18. build_priority_queue
- Status: OK
- Command: `python -m app.build_priority_queue`
- File: `app/build_priority_queue.py`
- Logs:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/exploration_v2.json`
  - `app/logs/product_performance.json`

### 19. publish_execution_plan
- Status: OK
- Command: `python -m app.publish_execution_plan`
- File: `app/publish_execution_plan.py`
- Logs:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/publish_execution_plan.json`

### 20. trend_listing_validator
- Status: MISSING
- Command: `python -m app.trend_listing_validator`
- File: `app/trend_listing_validator.py`

### 21. cj_trend_bridge
- Status: MISSING
- Command: `python -m app.cj_trend_bridge`
- File: `app/cj_trend_bridge.py`

### 22. supplier_candidate_filter
- Status: MISSING
- Command: `python app/filter_supplier_candidates.py`
- File: `app/filter_supplier_candidates.py`

### 23. seo_product_optimizer
- Status: MISSING
- Command: `python -m app.seo_product_optimizer`
- File: `app/seo_product_optimizer.py`

### 24. profit_checked_products
- Status: MISSING
- Command: `python -m app.profit_checked_products`
- File: `app/profit_checked_products.py`

### 25. action_executor
- Status: OK
- Command: `python -m app.action_executor`
- File: `app/action_executor.py`
- Logs:
  - `app/logs/action_executor.json`
  - `app/logs/publish_execution_plan.json`

### 26. social_content_generator
- Status: OK
- Command: `python -m app.social_content_generator`
- File: `app/social_content_generator.py`
- Logs:
  - `app/logs/publish_execution_plan.json`
  - `app/logs/social_content_plan.json`

### 27. social_content_enhancer
- Status: OK
- Command: `python -m app.social_content_enhancer`
- File: `app/social_content_enhancer.py`
- Logs:
  - `app/logs/social_content_enhanced.json`
  - `app/logs/social_content_plan.json`

### 28. auto_publish_or_fallback
- Status: OK
- Command: `python -m app.auto_publish_or_fallback`
- File: `app/auto_publish_or_fallback.py`
- ENV:
  - `META_PAGE_ACCESS_TOKEN`
  - `META_PAGE_ID`
- Logs:
  - `app/logs/auto_publish_or_fallback_result.json`
  - `app/logs/published_posts.json`

### 29. meta_ad_drafts_from_content
- Status: OK
- Command: `python -m app.meta_ad_drafts_from_content`
- File: `app/meta_ad_drafts_from_content.py`
- Logs:
  - `app/logs/meta_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 30. google_ad_drafts_from_content
- Status: OK
- Command: `python -m app.google_ad_drafts_from_content`
- File: `app/google_ad_drafts_from_content.py`
- Logs:
  - `app/logs/google_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 31. campaign_hub
- Status: OK
- Command: `python -m app.campaign_hub`
- File: `app/campaign_hub.py`
- Logs:
  - `app/logs/campaign_hub.json`
  - `app/logs/google_ad_drafts_from_content.json`
  - `app/logs/meta_ad_drafts_from_content.json`
  - `app/logs/social_content_enhanced.json`

### 32. campaign_approval_queue
- Status: OK
- Command: `python -m app.campaign_approval_queue`
- File: `app/campaign_approval_queue.py`
- Logs:
  - `app/logs/campaign_approval_queue.json`
  - `app/logs/campaign_hub.json`

### 33. system_status_report
- Status: OK
- Command: `python -m app.system_status_report`
- File: `app/system_status_report.py`
- Logs:
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

### 34. daily_summary
- Status: OK
- Command: `python -m app.daily_summary`
- File: `app/daily_summary.py`
- Logs:
  - `app/logs/autopilot_priority_queue.json`
  - `app/logs/autopilot_run.json`
  - `app/logs/product_performance.json`

### 35. auto_scaling_score
- Status: OK
- Command: `python -m app.auto_scaling_score`
- File: `app/auto_scaling_score.py`
- Logs:
  - `app/logs/auto_scaling_score.json`

### 36. product_guardrails
- Status: OK
- Command: `python -m app.product_guardrails`
- File: `app/product_guardrails.py`
- Logs:
  - `app/logs/product_guardrails.json`

### 37. roi_simulation
- Status: OK
- Command: `python -m app.roi_simulation`
- File: `app/roi_simulation.py`
- Logs:
  - `app/logs/auto_scaling_score.json`
  - `app/logs/roi_simulation.json`

### 38. ceo_dashboard
- Status: OK
- Command: `python -m app.ceo_dashboard`
- File: `app/ceo_dashboard.py`

### 39. auto_launch_engine
- Status: OK
- Command: `python -m app.auto_launch_engine`
- File: `app/auto_launch_engine.py`
- Logs:
  - `app/logs/auto_launch_decisions.json`
  - `app/logs/roi_simulation.json`

### 40. auto_spend_executor
- Status: OK
- Command: `python -m app.auto_spend_executor`
- File: `app/auto_spend_executor.py`
- Logs:
  - `app/logs/auto_launch_decisions.json`
  - `app/logs/auto_spend_executor.json`

### 41. spend_history_tracker
- Status: OK
- Command: `python -m app.spend_history_tracker`
- File: `app/spend_history_tracker.py`
- Logs:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/spend_history_tracker.json`

### 42. negative_roi_auto_pause
- Status: OK
- Command: `python -m app.negative_roi_auto_pause`
- File: `app/negative_roi_auto_pause.py`
- Logs:
  - `app/logs/negative_roi_auto_pause.json`
  - `app/logs/spend_history_tracker.json`

### 43. hourly_budget_monitor
- Status: OK
- Command: `python -m app.hourly_budget_monitor`
- File: `app/hourly_budget_monitor.py`
- Logs:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/hourly_budget_monitor.json`

### 44. emergency_stop_validator
- Status: OK
- Command: `python -m app.emergency_stop_validator`
- File: `app/emergency_stop_validator.py`
- Logs:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/emergency_stop_validator.json`
  - `app/logs/hourly_budget_monitor.json`

### 45. live_spend_permission_gate
- Status: OK
- Command: `python -m app.live_spend_permission_gate`
- File: `app/live_spend_permission_gate.py`
- Logs:
  - `app/logs/auto_spend_executor.json`
  - `app/logs/emergency_stop_validator.json`
  - `app/logs/live_spend_permission_gate.json`

### 46. live_backend_router
- Status: OK
- Command: `python -m app.live_backend_router`
- File: `app/live_backend_router.py`
- Logs:
  - `app/logs/live_backend_router.json`
  - `app/logs/live_spend_permission_gate.json`

### 47. meta_live_campaign_builder
- Status: OK
- Command: `python -m app.meta_live_campaign_builder`
- File: `app/meta_live_campaign_builder.py`
- Logs:
  - `app/logs/live_backend_router.json`
  - `app/logs/meta_live_campaign_payloads.json`

### 48. google_live_campaign_builder
- Status: OK
- Command: `python -m app.google_live_campaign_builder`
- File: `app/google_live_campaign_builder.py`
- Logs:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_backend_router.json`

### 49. live_campaign_registry
- Status: OK
- Command: `python -m app.live_campaign_registry`
- File: `app/live_campaign_registry.py`
- Logs:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/live_campaign_registry.json`
  - `app/logs/meta_live_campaign_payloads.json`

### 50. live_api_execution_gate
- Status: OK
- Command: `python -m app.live_api_execution_gate`
- File: `app/live_api_execution_gate.py`
- Logs:
  - `app/logs/live_api_execution_gate.json`
  - `app/logs/live_campaign_registry.json`
  - `app/logs/live_spend_permission_gate.json`

### 51. live_execution_reporter
- Status: OK
- Command: `python -m app.live_execution_reporter`
- File: `app/live_execution_reporter.py`
- Logs:
  - `app/logs/live_api_execution_gate.json`
  - `app/logs/live_execution_report.json`

### 52. live_mode_final_lock
- Status: OK
- Command: `python -m app.live_mode_final_lock`
- File: `app/live_mode_final_lock.py`
- Logs:
  - `app/logs/live_execution_report.json`
  - `app/logs/live_mode_final_lock.json`

### 53. meta_long_lived_token
- Status: MISSING
- Command: `python -m app.meta_long_lived_token`
- File: `app/meta_long_lived_token.py`

### 54. meta_live_executor
- Status: OK
- Command: `python -m app.meta_live_executor`
- File: `app/meta_live_executor.py`
- ENV:
  - `META_ACCESS_TOKEN`
  - `META_AD_ACCOUNT_ID`
  - `META_API_VERSION`
- Logs:
  - `app/logs/live_mode_final_lock.json`
  - `app/logs/meta_live_campaign_payloads.json`
  - `app/logs/meta_live_execution_result.json`

### 55. google_live_executor
- Status: OK
- Command: `python -m app.google_live_executor`
- File: `app/google_live_executor.py`
- Logs:
  - `app/logs/google_live_campaign_payloads.json`
  - `app/logs/google_live_execution_result.json`
  - `app/logs/live_mode_final_lock.json`

### 56. live_execution_consolidator
- Status: OK
- Command: `python -m app.live_execution_consolidator`
- File: `app/live_execution_consolidator.py`
- Logs:
  - `app/logs/google_live_execution_result.json`
  - `app/logs/live_execution_consolidated.json`
  - `app/logs/meta_live_execution_result.json`

### 57. live_spend_audit_ledger
- Status: OK
- Command: `python -m app.live_spend_audit_ledger`
- File: `app/live_spend_audit_ledger.py`
- Logs:
  - `app/logs/live_execution_consolidated.json`
  - `app/logs/live_spend_audit_ledger.jsonl`

### 58. live_spend_audit_reader
- Status: OK
- Command: `python -m app.live_spend_audit_reader`
- File: `app/live_spend_audit_reader.py`
- Logs:
  - `app/logs/live_spend_audit_ledger.jsonl`

### 59. send_daily_summary
- Status: OK
- Command: `python -m app.send_daily_summary`
- File: `app/send_daily_summary.py`
- ENV:
  - `OWNER_EMAIL`
  - `SMTP_FROM_EMAIL`
  - `SMTP_HOST`
  - `SMTP_PASSWORD`
  - `SMTP_PORT`
  - `SMTP_USER`
- Logs:
  - `app/logs/send_daily_summary.json`

### 60. send_telegram_summary
- Status: OK
- Command: `python -m app.send_telegram_summary`
- File: `app/send_telegram_summary.py`
- ENV:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
- Logs:
  - `app/logs/send_telegram_summary.json`

### 61. customer_fulfillment_support_status
- Status: MISSING
- Command: `python -m app.customer_fulfillment_support_status`
- File: `app/customer_fulfillment_support_status.py`

### 62. env_backup_sync
- Status: MISSING
- Command: `powershell Copy-Item .env .env.backup -Force`
- File: `None`

### 63. env_channel_recovery
- Status: MISSING
- Command: `python -m app.env_channel_recovery`
- File: `app/env_channel_recovery.py`

### 64. refresh_shopify_token
- Status: OK
- Command: `python -m app.refresh_shopify_token`
- File: `app/refresh_shopify_token.py`
- Logs:
  - `app/logs/shopify_token_refresh.json`

### 65. railway_env_sync
- Status: MISSING
- Command: `python -m app.railway_env_sync`
- File: `app/railway_env_sync.py`

### 66. listing_publish_execution_plan_real
- Status: MISSING
- Command: `python -m app.listing_publish_execution_plan_real`
- File: `app/listing_publish_execution_plan_real.py`

### 67. marketplace_listing_publisher
- Status: MISSING
- Command: `python -m app.marketplace_listing_publisher`
- File: `app/marketplace_listing_publisher.py`

### 68. draft_listing_activation_plan
- Status: MISSING
- Command: `python -m app.draft_listing_activation_plan`
- File: `app/draft_listing_activation_plan.py`

### 69. draft_listing_activator
- Status: MISSING
- Command: `python -m app.draft_listing_activator`
- File: `app/draft_listing_activator.py`

### 70. marketplace_order_autobuy
- Status: MISSING
- Command: `python -m app.marketplace_order_autobuy`
- File: `app/marketplace_order_autobuy.py`

### 71. autonomous_fulfillment_status
- Status: OK
- Command: `python -m app.autonomous_fulfillment_status`
- File: `app/autonomous_fulfillment_status.py`
- Logs:
  - `app/logs/autonomous_fulfillment_status.json`
  - `app/logs/autonomy_limits.json`
  - `app/logs/supplier_purchase_queue.json`

## Missing Modules

- `railway_health_check` ? `app/railway_health_check.py`
- `cj_paid_order_fulfillment` ? `app/cj_paid_order_fulfillment.py`
- `real_trend_discovery` ? `app/real_trend_discovery.py`
- `autonomous_trend_filter` ? `app/autonomous_trend_filter.py`
- `trend_listing_validator` ? `app/trend_listing_validator.py`
- `cj_trend_bridge` ? `app/cj_trend_bridge.py`
- `supplier_candidate_filter` ? `app/filter_supplier_candidates.py`
- `seo_product_optimizer` ? `app/seo_product_optimizer.py`
- `profit_checked_products` ? `app/profit_checked_products.py`
- `meta_long_lived_token` ? `app/meta_long_lived_token.py`
- `customer_fulfillment_support_status` ? `app/customer_fulfillment_support_status.py`
- `env_backup_sync` ? `None`
- `env_channel_recovery` ? `app/env_channel_recovery.py`
- `railway_env_sync` ? `app/railway_env_sync.py`
- `listing_publish_execution_plan_real` ? `app/listing_publish_execution_plan_real.py`
- `marketplace_listing_publisher` ? `app/marketplace_listing_publisher.py`
- `draft_listing_activation_plan` ? `app/draft_listing_activation_plan.py`
- `draft_listing_activator` ? `app/draft_listing_activator.py`
- `marketplace_order_autobuy` ? `app/marketplace_order_autobuy.py`

## Recommended Core Flow

1. Token refresh and channel health
2. Sales and CRM collection
3. Product discovery
4. Priority queue
5. Publish execution plan
6. Product guardrails
7. Content generation
8. Campaign draft generation
9. ROI and budget safety
10. Live execution in paused/safe mode
11. Reporting
12. Fulfillment and supplier purchase after paid order