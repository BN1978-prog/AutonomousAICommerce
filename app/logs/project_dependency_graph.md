# Project Dependency Graph

Created at: 2026-06-29T20:26:15.655880+00:00
Files: 721

## Autopilot-called modules

### `app/action_executor.py`
- Called by: app/autopilot_runner.py, app/patch_social_content_generator.py
- Logs: app/logs/action_executor.json, app/logs/publish_execution_plan.json

### `app/amazon_token_refresher.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py
- Logs: app/logs/amazon_token_refresher.json
- ENV: AMAZON_LWA_CLIENT_ID, AMAZON_LWA_CLIENT_SECRET, AMAZON_REFRESH_TOKEN

### `app/auto_launch_engine.py`
- Called by: app/autopilot_runner.py, app/patch_auto_spend_runner.py
- Logs: app/logs/auto_launch_decisions.json, app/logs/roi_simulation.json

### `app/auto_publish_or_fallback.py`
- Called by: app/autopilot_runner.py
- Logs: app/logs/auto_publish_or_fallback_result.json, app/logs/published_posts.json
- ENV: META_PAGE_ACCESS_TOKEN, META_PAGE_ID

### `app/auto_scaling_score.py`
- Called by: app/autopilot_runner.py, app/patch_auto_scaling_runner.py, app/patch_guardrails_runner.py
- Logs: app/logs/auto_scaling_score.json

### `app/auto_spend_executor.py`
- Called by: app/autopilot_runner.py, app/patch_auto_spend_runner.py, app/patch_spend_history_runner.py
- Logs: app/logs/auto_launch_decisions.json, app/logs/auto_spend_executor.json

### `app/autonomous_fulfillment_status.py`
- Called by: app/autopilot_runner.py
- Logs: app/logs/autonomous_fulfillment_status.json, app/logs/autonomy_limits.json, app/logs/supplier_purchase_queue.json

### `app/build_priority_queue.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_priority_queue.py, app/patch_autopilot_publish_plan.py, app/patch_pre_guard_planning.py
- Logs: app/logs/autopilot_priority_queue.json, app/logs/exploration_v2.json, app/logs/product_performance.json

### `app/campaign_approval_queue.py`
- Called by: app/autopilot_runner.py, app/patch_campaign_approval_queue.py
- Logs: app/logs/campaign_approval_queue.json, app/logs/campaign_hub.json

### `app/campaign_hub.py`
- Called by: app/autopilot_runner.py, app/patch_campaign_approval_queue.py, app/patch_campaign_hub.py
- Logs: app/logs/campaign_hub.json, app/logs/google_ad_drafts_from_content.json, app/logs/meta_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app/ceo_dashboard.py`
- Called by: app/autopilot_runner.py, app/patch_auto_spend_runner.py, app/patch_ceo_dashboard_runner.py

### `app/crm_personalized_drafts.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_crm_drafts.py
- Logs: app/logs/crm_personalized_drafts.json, app/logs/shopify_crm_events.json

### `app/crm_readiness_summary.py`
- Called by: app/autopilot_runner.py, app/control_panel.py, app/fix_autopilot_indent.py, app/patch_autopilot_etsy.py, app/patch_pre_guard_planning.py
- Logs: app/logs/crm_channel_readiness.json, app/logs/crm_health_check.json, app/logs/crm_queue.json, app/logs/crm_readiness_summary.json, app/logs/crm_send_guard.json, app/logs/smtp_config_validator.json

### `app/daily_publish_guard.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_shopify_refresh.py
- Logs: app/logs/daily_publish_lock.json

### `app/daily_summary.py`
- Called by: app/autopilot_runner.py, app/fix_report_order.py, app/patch_auto_scaling_runner.py, app/patch_autopilot_crm_drafts.py, app/patch_autopilot_system_status.py, app/patch_send_daily_summary.py
- Logs: app/logs/autopilot_priority_queue.json, app/logs/autopilot_run.json, app/logs/product_performance.json

### `app/emergency_stop_validator.py`
- Called by: app/autopilot_runner.py, app/patch_emergency_stop_runner.py, app/patch_live_gate_runner.py
- Logs: app/logs/auto_spend_executor.json, app/logs/emergency_stop_validator.json, app/logs/hourly_budget_monitor.json

### `app/etsy_autopilot.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py, app/fix_autopilot_indent.py, app/patch_autopilot_etsy.py
- Logs: app/logs/etsy_autopilot.json
- ENV: ETSY_ACCESS_TOKEN

### `app/etsy_connection_status.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py, app/fix_autopilot_indent.py, app/patch_autopilot_etsy.py
- Logs: app/logs/etsy_connection_status.json

### `app/exploration_engine_v2.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_exploration_v2.py, app/patch_autopilot_priority_queue.py, app/patch_pre_guard_planning.py
- Logs: app/logs/exploration_v2.json, app/logs/product_performance.json

### `app/google_ad_drafts_from_content.py`
- Called by: app/autopilot_runner.py, app/patch_campaign_hub.py, app/patch_google_ad_drafts.py
- Logs: app/logs/google_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app/google_ads_token_refresher.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py
- Logs: app/logs/google_ads_token_refresher.json
- ENV: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN

### `app/google_live_campaign_builder.py`
- Called by: app/autopilot_runner.py, app/patch_google_live_builder_runner.py, app/patch_live_campaign_registry_runner.py
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/live_backend_router.json

### `app/google_live_executor.py`
- Called by: app/autopilot_runner.py, app/patch_live_consolidator_runner.py, app/patch_live_executors_runner.py
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/google_live_execution_result.json, app/logs/live_mode_final_lock.json

### `app/hourly_budget_monitor.py`
- Called by: app/autopilot_runner.py, app/patch_emergency_stop_runner.py, app/patch_hourly_budget_runner.py
- Logs: app/logs/auto_spend_executor.json, app/logs/hourly_budget_monitor.json

### `app/live_api_execution_gate.py`
- Called by: app/autopilot_runner.py, app/patch_live_api_gate_runner.py, app/patch_live_execution_reporter_runner.py
- Logs: app/logs/live_api_execution_gate.json, app/logs/live_campaign_registry.json, app/logs/live_spend_permission_gate.json

### `app/live_backend_router.py`
- Called by: app/autopilot_runner.py, app/patch_live_backend_router_runner.py, app/patch_meta_live_builder_runner.py
- Logs: app/logs/live_backend_router.json, app/logs/live_spend_permission_gate.json

### `app/live_campaign_registry.py`
- Called by: app/autopilot_runner.py, app/patch_live_api_gate_runner.py, app/patch_live_campaign_registry_runner.py
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/live_campaign_registry.json, app/logs/meta_live_campaign_payloads.json

### `app/live_execution_consolidator.py`
- Called by: app/autopilot_runner.py, app/patch_live_audit_ledger_runner.py, app/patch_live_consolidator_runner.py
- Logs: app/logs/google_live_execution_result.json, app/logs/live_execution_consolidated.json, app/logs/meta_live_execution_result.json

### `app/live_execution_reporter.py`
- Called by: app/autopilot_runner.py, app/patch_live_execution_reporter_runner.py, app/patch_live_mode_final_lock_runner.py
- Logs: app/logs/live_api_execution_gate.json, app/logs/live_execution_report.json

### `app/live_mode_final_lock.py`
- Called by: app/autopilot_runner.py, app/patch_live_executors_runner.py, app/patch_live_mode_final_lock_runner.py
- Logs: app/logs/live_execution_report.json, app/logs/live_mode_final_lock.json

### `app/live_spend_audit_ledger.py`
- Called by: app/autopilot_runner.py, app/patch_live_audit_ledger_runner.py, app/patch_live_audit_reader_runner.py
- Logs: app/logs/live_execution_consolidated.json, app/logs/live_spend_audit_ledger.jsonl

### `app/live_spend_audit_reader.py`
- Called by: app/autopilot_runner.py, app/patch_live_audit_reader_runner.py
- Logs: app/logs/live_spend_audit_ledger.jsonl

### `app/live_spend_permission_gate.py`
- Called by: app/autopilot_runner.py, app/patch_live_backend_router_runner.py, app/patch_live_gate_runner.py
- Logs: app/logs/auto_spend_executor.json, app/logs/emergency_stop_validator.json, app/logs/live_spend_permission_gate.json

### `app/meta_ad_drafts_from_content.py`
- Called by: app/autopilot_runner.py, app/patch_google_ad_drafts.py, app/patch_meta_ad_drafts.py
- Logs: app/logs/meta_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app/meta_live_campaign_builder.py`
- Called by: app/autopilot_runner.py, app/patch_google_live_builder_runner.py, app/patch_meta_live_builder_runner.py
- Logs: app/logs/live_backend_router.json, app/logs/meta_live_campaign_payloads.json

### `app/meta_live_executor.py`
- Called by: app/autopilot_runner.py, app/patch_live_executors_runner.py
- Logs: app/logs/live_mode_final_lock.json, app/logs/meta_live_campaign_payloads.json, app/logs/meta_live_execution_result.json
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION

### `app/meta_page_token_refresh.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py
- Logs: app/logs/meta_page_token_refresh.json
- ENV: META_ACCESS_TOKEN, META_PAGE_ID

### `app/meta_token_refresh.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py
- Logs: app/logs/meta_token_refresh.json

### `app/negative_roi_auto_pause.py`
- Called by: app/autopilot_runner.py, app/patch_hourly_budget_runner.py, app/patch_negative_roi_runner.py
- Logs: app/logs/negative_roi_auto_pause.json, app/logs/spend_history_tracker.json

### `app/product_guardrails.py`
- Called by: app/autopilot_runner.py, app/patch_guardrails_runner.py, app/patch_roi_runner.py
- Logs: app/logs/product_guardrails.json

### `app/publish_execution_plan.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_publish_plan.py, app/patch_pre_guard_planning.py
- Logs: app/logs/autopilot_priority_queue.json, app/logs/publish_execution_plan.json

### `app/real_sales_collector.py`
- Called by: app/autopilot_runner.py
- Logs: app/logs/imported_skus.json, app/logs/real_sales_report.json
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_OAUTH_TOKEN, EBAY_USER_TOKEN, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET, WC_STORE_URL, WOOCOMMERCE_CONSUMER_KEY

### `app/refresh_ebay_token.py`
- Called by: app/autopilot_runner.py
- ENV: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN

### `app/refresh_shopify_token.py`
- Called by: app/autopilot_runner.py, app/channel_sync_manager.py, app/patch_autopilot_shopify_refresh.py
- Logs: app/logs/shopify_token_refresh.json

### `app/roi_simulation.py`
- Called by: app/autopilot_runner.py, app/patch_ceo_dashboard_runner.py, app/patch_roi_runner.py
- Logs: app/logs/auto_scaling_score.json, app/logs/roi_simulation.json

### `app/send_daily_summary.py`
- Called by: app/autopilot_runner.py, app/patch_send_daily_summary.py, app/patch_telegram_summary.py
- Logs: app/logs/send_daily_summary.json
- ENV: OWNER_EMAIL, SMTP_FROM_EMAIL, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER

### `app/send_telegram_alert.py`
- Called by: app/autopilot_runner.py
- ENV: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

### `app/send_telegram_summary.py`
- Called by: app/add_forced_error.py, app/autopilot_runner.py, app/patch_telegram_summary.py
- Logs: app/logs/send_telegram_summary.json
- ENV: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

### `app/shopify_crm_events.py`
- Called by: app/autopilot_runner.py, app/patch_autopilot_crm_drafts.py
- Logs: app/logs/shopify_crm_events.json
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL

### `app/social_content_enhancer.py`
- Called by: app/autopilot_runner.py, app/patch_meta_ad_drafts.py, app/patch_social_content_enhancer.py
- Logs: app/logs/social_content_enhanced.json, app/logs/social_content_plan.json

### `app/social_content_generator.py`
- Called by: app/autopilot_runner.py, app/patch_social_content_enhancer.py, app/patch_social_content_generator.py
- Logs: app/logs/publish_execution_plan.json, app/logs/social_content_plan.json

### `app/spend_history_tracker.py`
- Called by: app/autopilot_runner.py, app/patch_negative_roi_runner.py, app/patch_spend_history_runner.py
- Logs: app/logs/auto_spend_executor.json, app/logs/spend_history_tracker.json

### `app/system_status_report.py`
- Called by: app/autopilot_runner.py, app/control_panel.py, app/fix_report_order.py, app/patch_autopilot_system_status.py
- Logs: app/logs/action_executor.json, app/logs/amazon_connection_status.json, app/logs/autopilot_priority_queue.json, app/logs/autopilot_run.json, app/logs/crm_readiness_summary.json, app/logs/etsy_autopilot.json, app/logs/etsy_connection_status.json, app/logs/google_campaign_live_creator.json, app/logs/master_system_health.json, app/logs/meta_launch_readiness.json

### `app/token_manager.py`
- Called by: app/autopilot_runner.py
- Logs: app/logs/token_manager_status.json
- ENV: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN, META_ACCESS_TOKEN, META_APP_ID, META_APP_SECRET, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN

## Files with no detected caller

- `app/__init__.py`
- `app/ad_campaign_executor.py`
- `app/adaptation/__init__.py`
- `app/add_created_at_to_skus.py`
- `app/add_forced_error.py`
- `app/add_product_results.py`
- `app/add_test_tracking.py`
- `app/ai_pricing_engine.py`
- `app/ai_score_report.py`
- `app/alerts_engine.py`
- `app/aliexpress_connection_status.py`
- `app/aliexpress_scanner.py`
- `app/amazon_auth_url.py`
- `app/amazon_oauth_exchange.py`
- `app/amazon_scanner.py`
- `app/apply_scale_limits.py`
- `app/apply_utm_to_social_posts.py`
- `app/arbitrage_decisions.py`
- `app/arbitrage_execution_plan.py`
- `app/arbitrage_safety_gate.py`
- `app/assign_local_images.py`
- `app/auto_disable_skus.py`
- `app/auto_free_traffic_launcher.py`
- `app/automation/__init__.py`
- `app/autonomous_loop_health.py`
- `app/autonomous_order_router.py`
- `app/autopilot_schedule_readiness.py`
- `app/backup_manager.py`
- `app/blocked_report.py`
- `app/budget_controller.py`
- `app/budget_mode_detector.py`
- `app/budget_scaling_rules.py`
- `app/campaign_executor.py`
- `app/catalog_filter.py`
- `app/catalog_final_filter.py`
- `app/channel_live_test.py`
- `app/channel_performance.py`
- `app/channel_validation.py`
- `app/channel_validation_checkpoint.py`
- `app/channels/__init__.py`
- `app/channels/amazon_adapter.py`
- `app/channels/base.py`
- `app/channels/base_adapter.py`
- `app/channels/channel_manager.py`
- `app/channels/channel_registry.py`
- `app/channels/ebay_adapter.py`
- `app/channels/ebay_gateway_ACCESS_TOKEN_OK.py`
- `app/channels/ebay_gateway_CONNECTED_OK.py`
- `app/channels/ebay_gateway_INVENTORY_ITEM_OK.py`
- `app/channels/etsy_adapter.py`
- `app/channels/google_merchant_adapter.py`
- `app/channels/meta_shop_adapter.py`
- `app/channels/registry.py`
- `app/channels/shopify_adapter.py`
- `app/channels/tiktok_adapter.py`
- `app/channels/tiktok_shop_adapter.py`
- `app/channels/walmart_adapter.py`
- `app/channels/woocommerce_adapter.py`
- `app/check_cj_status.py`
- `app/check_ebay_env_safe.py`
- `app/check_meta_ads.py`
- `app/check_meta_adsets.py`
- `app/cj_customer_address_validator.py`
- `app/cj_order_draft_creator.py`
- `app/cj_payload_builder.py`
- `app/cj_product_detail.py`
- `app/cj_product_search.py`
- `app/cj_purchase_executor.py`
- `app/cj_supplier_readiness.py`
- `app/clean_catalog.py`
- `app/cleanup_forced_error.py`
- `app/cleanup_logs.py`
- `app/cleanup_pricing_candidates.py`
- `app/clear_test_orders.py`
- `app/click_tracking_init.py`
- `app/collect_ebay_orders.py`
- `app/collect_incoming_orders.py`
- `app/collect_shopify_orders.py`
- `app/collect_woocommerce_orders.py`
- `app/commerce/__init__.py`
- `app/commerce/routes_4_CHANNELS_CONNECTED_OK.py`
- `app/commerce/routes_6_CHANNELS_READY_OK.py`
- `app/commerce/routes_EBAY_CONNECTED_OK.py`
- `app/commerce/routes_EBAY_OVERVIEW_CONNECTED_OK.py`
- `app/commerce/routes_MULTI_CHANNEL_FINAL_OK.py`
- `app/commerce/routes_OVERVIEW_OK.py`
- `app/commerce/routes_REAL_OVERVIEW_OK.py`
- `app/commerce/routes_UNIQUE_TOTALS_OK.py`
- `app/compliance_layer.py`
- `app/connect_crm_smtp_draft.py`
- `app/conversion_tracking_validation.py`
- `app/conversion_watch.py`
- `app/crm_action_planner.py`
- `app/crm_automation.py`
- `app/crm_channel_readiness.py`
- `app/crm_confirm_owner_for_test.py`
- `app/crm_draft_outbox.py`
- `app/crm_event_router.py`
- `app/crm_executor_dry_run.py`
- `app/crm_final_gate.py`
- `app/crm_health_check.py`
- `app/crm_message_generator.py`
- `app/crm_orchestrator.py`
- `app/crm_prepare_single_test.py`
- `app/crm_provider_config_check.py`
- `app/crm_queue_builder.py`
- `app/crm_send_guard.py`
- `app/crm_send_one_test.py`
- `app/customer_analytics.py`
- `app/customer_segmentation.py`
- `app/daily_decision_report.py`
- `app/daily_free_traffic_tasks.py`
- `app/daily_report.py`
- `app/daily_run.py`
- `app/dashboard/__init__.py`
- `app/dashboard_report.py`
- `app/debug_pipeline.py`
- `app/debug_shopify_crm_source.py`
- `app/debug_shopify_env.py`
- `app/decision_engine.py`
- `app/delete_shopify_duplicate.py`
- `app/deployment_readiness_checklist.py`
- `app/deployment_summary.py`
- `app/disable_candidates.py`
- `app/download_dog_socks_image.py`
- `app/download_product_images.py`
- `app/dynamic_product_score.py`
- `app/dynamic_score_sync.py`
- `app/ebay_read_validation.py`
- `app/ebay_write_offer_validation.py`
- `app/ebay_write_validation.py`
- `app/enable_crm_limited_send.py`
- `app/engines/__init__.py`
- `app/engines/action_executor.py`
- `app/engines/automation_daemon_worker.py`
- `app/engines/automation_log.py`
- `app/engines/automation_rules.py`
- `app/engines/automation_ruleset_loader.py`
- `app/engines/automation_state.py`
- `app/engines/automation_tick.py`
- `app/engines/compliance.py`
- `app/engines/daemon_restore.py`
- `app/engines/decision_logger.py`
- `app/engines/decision_memory.py`
- `app/engines/demand.py`
- `app/engines/executor.py`
- `app/engines/global_commerce_brain.py`
- `app/engines/guard.py`
- `app/engines/marketplace.py`
- `app/engines/marketplace_scoring.py`
- `app/engines/pricing.py`
- `app/engines/product_lookup.py`
- `app/engines/queue.py`
- `app/engines/risk_guard.py`
- `app/engines/routing.py`
- `app/engines/rule_engine.py`
- `app/engines/seo.py`
- `app/engines/wallet_engine.py`
- `app/etsy_auth_url.py`
- `app/etsy_oauth_exchange.py`
- `app/event_collector_state.py`
- `app/event_learning_sync.py`
- `app/example.py`
- `app/expand_catalog.py`
- `app/external_blockers_monitor.py`
- `app/external_platform_blockers.py`
- `app/feed_channel_validation.py`
- `app/feed_mass_regenerator.py`
- `app/feed_quality_check.py`
- `app/feed_regenerator.py`
- `app/feeds/__init__.py`
- `app/feeds/google_merchant_feed.py`
- `app/feeds/meta_feed.py`
- `app/final_mvp/__init__.py`
- `app/final_system_check.py`
- `app/final_system_checkpoint.py`
- `app/finance/__init__.py`
- `app/fix_autopilot_crm_duplicates.py`
- `app/fix_autopilot_indent.py`
- `app/fix_bom_campaign_queue.py`
- `app/fix_error_handler.py`
- `app/fix_meta_account_id.py`
- `app/fix_meta_budget_sharing.py`
- `app/fix_meta_objective.py`
- `app/fix_meta_special_categories.py`
- `app/fix_report_order.py`
- `app/fix_unicode_report.py`
- `app/fix_woocommerce_validation_url.py`
- `app/fulfillment/__init__.py`
- `app/fulfillment_status_report.py`
- `app/full_system_final_run.py`
- `app/generate_product_images.py`
- `app/generate_publish_queue.py`
- `app/global_arbitrage_engine.py`
- `app/global_channel_requirements_check.py`
- `app/global_channel_status_summary.py`
- `app/global_commerce_control_panel.py`
- `app/global_execution_plan.py`
- `app/global_marketplace_roadmap.py`
- `app/google_access_monitor.py`
- `app/google_activation_readiness_gate.py`
- `app/google_ads_readiness.py`
- `app/google_campaign_live_creator.py`
- `app/google_campaign_live_poster.py`
- `app/google_payload_safe_creator.py`
- `app/google_refresh_token.py`
- `app/health_check.py`
- `app/hunter_action_executor.py`
- `app/hunter_action_plan.py`
- `app/hunter_feedback_engine.py`
- `app/hunter_import.py`
- `app/hunter_registry_sync.py`
- `app/import_report.py`
- `app/import_shopify_products.py`
- `app/import_shopify_results.py`
- `app/import_supplier_products.py`
- `app/insert_winner_notify.py`
- `app/inventory_sync_guard.py`
- `app/listing_publish_execution_plan.py`
- `app/listing_publish_validator.py`
- `app/listing_publisher_plan.py`
- `app/listings/__init__.py`
- `app/main_AUTOPILOT_NO_DUPES_OK.py`
- `app/main_AUTOPILOT_SAFE_FLOW_OK.py`
- `app/main_CATALOG_HEALTH_OK.py`
- `app/main_CLEAN_CATALOG_OK.py`
- `app/main_DASHBOARD_WORKING_OK.py`
- `app/main_SAFE_FLOW_OK.py`
- `app/main_WITH_SHOPIFY_AUTO_MODULE_OK.py`
- `app/main_WORKING_DEDUPE_OK.py`
- `app/main_WORKING_SHOPIFY_OK.py`
- `app/main_backup.py`
- `app/main_before_shopify_fallback.py`
- `app/main_broken_20260518_112242.py`
- `app/main_restored.py`
- `app/margin_engine.py`
- `app/mark_manual_social_posts.py`
- `app/market_arbitrage_engine.py`
- `app/marketplaces/__init__.py`
- `app/meta_activate_ad.py`
- `app/meta_activate_adset.py`
- `app/meta_activate_campaign.py`
- `app/meta_activation_executor.py`
- `app/meta_activation_readiness_gate.py`
- `app/meta_ad_accounts.py`
- `app/meta_ad_builder.py`
- `app/meta_ads_live_creator.py`
- `app/meta_ads_readiness.py`
- `app/meta_adset_builder.py`
- `app/meta_adset_live_creator.py`