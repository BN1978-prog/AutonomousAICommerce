# AICommerce Project Architecture Audit

Created at: 2026-06-29T20:20:53.673746+00:00
Python files: 721

## ???? ??????? ? ???????? ????????

### `app\collect_ebay_orders.py`
- Lines: 71
- Logs: app/logs/ebay_orders.json

### `app\collect_incoming_orders.py`
- Lines: 50
- Logs: app/logs/ebay_orders.json, app/logs/incoming_orders.json, app/logs/shopify_orders.json, app/logs/woocommerce_orders.json

### `app\collect_shopify_orders.py`
- Lines: 88
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL
- Logs: app/logs/shopify_orders.json

### `app\collect_woocommerce_orders.py`
- Lines: 98
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_KEY, WOOCOMMERCE_SECRET, WOOCOMMERCE_STORE_URL, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_orders.json

### `app\shopify_order_address_collector.py`
- Lines: 109
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_API_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_DOMAIN, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL
- Logs: app/logs/shopify_order_address_collector.json, app/logs/shopify_order_addresses.json

### `app\shopify_orders_collector.py`
- Lines: 91
- Functions: load_env, normalize_shop
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL
- Logs: app/logs/shopify_orders_sales.json

## ?????? / ?????????????

### `app\autonomous_order_router.py`
- Lines: 70
- Logs: app/logs/autonomous_order_router.json, app/logs/autonomy_limits.json, app/logs/incoming_orders.json, app/logs/supplier_purchase_queue.json

### `app\clear_test_orders.py`
- Lines: 23
- Logs: app/logs/incoming_orders.json, app/logs/incoming_orders_TEST_BACKUP.json

### `app\fix_report_order.py`
- Lines: 16
- Runs steps: daily_summary, system_status_report

### `app\order_orchestrator.py`
- Lines: 49
- Logs: app/logs/imported_skus.json, app/logs/order_orchestration_plan.json

### `app\shopify_automation\orders.py`
- Lines: 30
- Functions: normalize_order

### `app\shopify_automation\orders_OK.py`
- Lines: 30
- Functions: normalize_order

## ?????? ???? / ????????

### `app\ai_pricing_engine.py`
- Lines: 62
- Functions: read_json
- Logs: app/logs/ai_pricing_engine.json, app/logs/global_arbitrage_engine.json

### `app\cleanup_pricing_candidates.py`
- Lines: 15
- Logs: app/logs/pricing_experiments.json

### `app\engines\pricing.py`
- Lines: 94

### `app\pricing_ai.py`
- Lines: 26
- Functions: dynamic_price

### `app\pricing_apply_safe.py`
- Lines: 33
- Logs: app/logs/pricing_apply_safe_report.json, app/logs/pricing_experiments.json

### `app\pricing_experiments.py`
- Lines: 55
- Logs: app/logs/pricing_experiments.json, app/logs/promotion_candidates.json

### `app\services\pricing_agent.py`
- Lines: 9
- Classes: PricingAgent
- Functions: recommend_price

### `app\shopify_automation\pricing.py`
- Lines: 47
- Functions: round_to_99, calculate_optimized_price

### `app\shopify_automation\pricing_OK.py`
- Lines: 47
- Functions: round_to_99, calculate_optimized_price

### `app\shopify_automation\routes_PRICING_OK.py`
- Lines: 436
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\suppliers\pricing.py`
- Lines: 12

### `patch_dynamic_pricing_import.py`
- Lines: 31

## ?????? ??????? / ROI / ?????

### `app\finance\advanced_profit_engine.py`
- Lines: 116
- Classes: AdvancedProfitEngine
- Functions: calculate, scenarios

### `app\margin_engine.py`
- Lines: 48
- Logs: app/logs/global_arbitrage_candidates.json, app/logs/opportunities/margin_report.json

### `app\negative_roi_auto_pause.py`
- Lines: 32
- Logs: app/logs/negative_roi_auto_pause.json, app/logs/spend_history_tracker.json

### `app\patch_negative_roi_runner.py`
- Lines: 17
- Runs steps: negative_roi_auto_pause, spend_history_tracker

### `app\patch_roi_runner.py`
- Lines: 17
- Runs steps: product_guardrails, roi_simulation

### `app\profit_report.py`
- Lines: 40

### `app\roi_engine.py`
- Lines: 46
- Functions: read_json
- Logs: app/logs/budget_controller.json, app/logs/real_sales_mode.json, app/logs/roi_engine.json, app/logs/system_status_dashboard.json

### `app\roi_report.py`
- Lines: 41
- Logs: app/logs/imported_skus.json, app/logs/roi_report.json

### `app\roi_simulation.py`
- Lines: 77
- Logs: app/logs/auto_scaling_score.json, app/logs/roi_simulation.json

### `app\sales_roi_engine.py`
- Lines: 103
- Logs: app/logs/imported_skus.json, app/logs/sales_roi_report.json

### `app\services\profit_engine.py`
- Lines: 37
- Classes: ProfitEngine
- Functions: calculate

### `tests\test_advanced_profit_risk.py`
- Lines: 115
- Functions: test_advanced_profit_engine_calculates_positive_margin, test_advanced_risk_engine_blocks_out_of_stock, test_advanced_governor_approves_strong_candidate, test_advanced_governor_rejects_bad_margin, test_advanced_evaluate_endpoint, test_profit_scenarios_endpoint_returns_three_scenarios

### `tests\test_profit_and_governor.py`
- Lines: 60
- Functions: make_product, test_profit_engine_calculates_positive_margin, test_governor_approves_good_product, test_governor_rejects_low_margin_product, test_governor_rejects_high_supplier_risk

## ??????? ?????? ?????????????

### `app\__init__.py`
- Lines: 0

### `app\action_executor.py`
- Lines: 47
- Logs: app/logs/action_executor.json, app/logs/publish_execution_plan.json

### `app\ad_campaign_executor.py`
- Lines: 56
- Logs: app/logs/CONFIRM_LIVE_ADS_LAUNCH.json, app/logs/ad_campaign_executor.json, app/logs/campaign_executor.json, app/logs/live_ads_guard.json

### `app\adaptation\__init__.py`
- Lines: 1

### `app\adaptation\engine.py`
- Lines: 185
- Classes: SelfLearningEngine
- Functions: analyze, _event_profit, _margin_percent, _rate, _entity_scores, _recommend

### `app\adaptation\schemas.py`
- Lines: 75
- Classes: OutcomeType, ProductPerformanceEvent, EntityScore, AdaptationRecommendation, LearningSummary, AdaptationRequest
- Functions: normalize_text

### `app\add_created_at_to_skus.py`
- Lines: 22
- Logs: app/logs/imported_skus.json

### `app\add_forced_error.py`
- Lines: 18
- Runs steps: forced_test_error, send_telegram_summary

### `app\add_product_results.py`
- Lines: 30
- Logs: app/logs/product_performance.json

### `app\ai_score_report.py`
- Lines: 51

### `app\alert_dispatcher.py`
- Lines: 57

### `app\alerts_engine.py`
- Lines: 80
- Functions: read_json
- Logs: app/logs/alerts.json, app/logs/daily_report.json, app/logs/external_blockers_monitor.json, app/logs/recovery_report.json, app/logs/system_status_dashboard.json

### `app\aliexpress_connection_status.py`
- Lines: 22
- Logs: app/logs/aliexpress_connection_status.json

### `app\aliexpress_scanner.py`
- Lines: 0

### `app\amazon_auth_url.py`
- Lines: 19
- ENV: AMAZON_LWA_CLIENT_ID, AMAZON_REDIRECT_URI

### `app\amazon_connection_status.py`
- Lines: 35
- Functions: read_json
- Logs: app/logs/amazon_connection_status.json, app/logs/global_channel_requirements_check.json

### `app\amazon_oauth_exchange.py`
- Lines: 82
- Functions: update_env
- ENV: AMAZON_AUTH_CODE, AMAZON_LWA_CLIENT_ID, AMAZON_LWA_CLIENT_SECRET
- Logs: app/logs/amazon_oauth_exchange.json

### `app\amazon_scanner.py`
- Lines: 0

### `app\amazon_token_refresher.py`
- Lines: 82
- Functions: update_env
- ENV: AMAZON_LWA_CLIENT_ID, AMAZON_LWA_CLIENT_SECRET, AMAZON_REFRESH_TOKEN
- Logs: app/logs/amazon_token_refresher.json

### `app\apply_scale_limits.py`
- Lines: 33
- Logs: app/logs/autopilot_decisions.json, app/logs/product_performance.json

### `app\apply_utm_to_social_posts.py`
- Lines: 44
- Logs: app/logs/daily_social_posts_ready.json, app/logs/daily_social_posts_with_utm.json

### `app\arbitrage_decisions.py`
- Lines: 52
- Logs: app/logs/arbitrage_decisions.json, app/logs/market_arbitrage_candidates.json

### `app\arbitrage_execution_plan.py`
- Lines: 45
- Logs: app/logs/arbitrage_execution_plan.json, app/logs/arbitrage_safety_gate.json

### `app\assign_local_images.py`
- Lines: 27
- Logs: app/logs/local_product_images.json

### `app\auto_disable_skus.py`
- Lines: 64
- Logs: app/logs/auto_disable_report.json, app/logs/blocked_products.json, app/logs/imported_skus.json

### `app\auto_free_traffic_launcher.py`
- Lines: 56
- Logs: app/logs/daily_social_posts_ready.json

### `app\auto_launch_engine.py`
- Lines: 43
- Logs: app/logs/auto_launch_decisions.json, app/logs/roi_simulation.json

### `app\auto_scaling_score.py`
- Lines: 75
- Logs: app/logs/auto_scaling_score.json

### `app\auto_spend_executor.py`
- Lines: 51
- Logs: app/logs/auto_launch_decisions.json, app/logs/auto_spend_executor.json

### `app\automation\__init__.py`
- Lines: 0

### `app\automation\schemas.py`
- Lines: 34
- Classes: SemiAutoRunRequest, SemiAutoProductResult, SemiAutoRunResult

### `app\automation\service.py`
- Lines: 144
- Classes: SemiAutoCommerceService
- Functions: __init__

### `app\autonomous_fulfillment_status.py`
- Lines: 41
- Logs: app/logs/autonomous_fulfillment_status.json, app/logs/autonomy_limits.json, app/logs/supplier_purchase_queue.json

### `app\autonomous_loop_health.py`
- Lines: 58
- Logs: app/logs/autonomous_loop_health.json, app/logs/imported_skus.json

### `app\backup_manager.py`
- Lines: 47
- Logs: app/logs/alerts.json, app/logs/backup_report.json, app/logs/daily_report.json, app/logs/external_blockers_monitor.json, app/logs/global_commerce_control_panel.json, app/logs/last_known_good_state.json, app/logs/production_readiness_report.json, app/logs/recovery_report.json, app/logs/system_status_dashboard.json

### `app\blocked_report.py`
- Lines: 36

### `app\budget_controller.py`
- Lines: 55
- Functions: read_json
- Logs: app/logs/budget_controller.json, app/logs/global_commerce_control_panel.json, app/logs/real_sales_mode.json, app/logs/system_status_dashboard.json

### `app\budget_mode_detector.py`
- Lines: 43
- Functions: read_json
- Logs: app/logs/available_balance.json, app/logs/budget_mode_detector.json

### `app\budget_scaling_rules.py`
- Lines: 29
- Logs: app/logs/budget_scaling_rules.json

### `app\build_priority_queue.py`
- Lines: 30
- Logs: app/logs/autopilot_priority_queue.json, app/logs/exploration_v2.json, app/logs/product_performance.json

### `app\campaign_approval_queue.py`
- Lines: 36
- Logs: app/logs/campaign_approval_queue.json, app/logs/campaign_hub.json

### `app\campaign_executor.py`
- Lines: 64
- Logs: app/logs/ad_spend_limits.json, app/logs/campaign_executor.json, app/logs/real_traffic_launcher.json

### `app\campaign_hub.py`
- Lines: 47
- Logs: app/logs/campaign_hub.json, app/logs/google_ad_drafts_from_content.json, app/logs/meta_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app\catalog_filter.py`
- Lines: 42
- Logs: app/logs/seo_mass_push_plan.json, app/logs/seo_mass_push_plan_filtered.json

### `app\catalog_final_filter.py`
- Lines: 50
- Logs: app/logs/seo_mass_push_plan_filtered.json, app/logs/seo_mass_push_plan_final.json

### `app\channel_health.py`
- Lines: 96
- Functions: _status, build_channel_health
- ENV: AMAZON_ACCESS_TOKEN, AMAZON_REFRESH_TOKEN, EBAY_ACCESS_TOKEN, EBAY_REFRESH_TOKEN, ETSY_ACCESS_TOKEN, ETSY_API_KEY, ETSY_CLIENT_ID, ETSY_SHOP_ID, GOOGLE_ADS_ACCESS_TOKEN, GOOGLE_ADS_REFRESH_TOKEN, META_ACCESS_TOKEN, OPENAI_API_KEY, SHOPIFY_ACCESS_TOKEN
- Logs: app/logs/channel_health.json, app/logs/shopify_token_auto_repair.json

### `app\channel_health_report.py`
- Lines: 36
- Logs: app/logs/blocked_products.json, app/logs/imported_skus.json, app/logs/stock_state.json

### `app\channel_live_test.py`
- Lines: 110
- Functions: load
- Logs: app/logs/channel_live_test.json, app/logs/channel_validation_checkpoint.json, app/logs/feed_channel_validation.json, app/logs/paid_ads_status.json, app/logs/real_sales_mode.json, app/logs/token_manager_status.json, app/logs/traffic_readiness.json

### `app\channel_performance.py`
- Lines: 52
- Logs: app/logs/channel_performance.json, app/logs/manual_channel_metrics.json

### `app\channel_self_healer.py`
- Lines: 171
- Functions: reload_env_from_file, run_module, parse_json, provider_problem, get_problems, main
- Logs: app/logs/channel_self_healer.json

### `app\channel_sync_manager.py`
- Lines: 92
- Functions: ensure_env_file, shopify_ok, sync_all_channels

### `app\channel_validation.py`
- Lines: 75
- Logs: app/logs/channel_validation.json, app/logs/imported_skus.json

### `app\channel_validation_checkpoint.py`
- Lines: 30
- Logs: app/logs/channel_validation_checkpoint.json, app/logs/ebay_write_offer_validation.json, app/logs/ebay_write_validation.json, app/logs/feed_channel_validation.json, app/logs/shopify_write_validation.json, app/logs/woocommerce_validation.json, app/logs/woocommerce_write_validation.json

### `app\channels\__init__.py`
- Lines: 0

### `app\channels\amazon_adapter.py`
- Lines: 24

### `app\channels\base.py`
- Lines: 49

### `app\channels\base_adapter.py`
- Lines: 45

### `app\channels\channel_manager.py`
- Lines: 472
- Functions: shopify_get_product_by_sku, shopify_get_product_details, shopify_publish_product, shopify_update_price, shopify_update_inventory, shopify_archive_product, run_channel_action, channel_token_check, all_channels_status
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_KEY, WOOCOMMERCE_SECRET, WOOCOMMERCE_STORE_URL, WOOCOMMERCE_URL

### `app\channels\channel_registry.py`
- Lines: 12

### `app\channels\registry.py`
- Lines: 53

### `app\channels\tiktok_adapter.py`
- Lines: 29

### `app\channels\tiktok_shop_adapter.py`
- Lines: 17

### `app\channels\walmart_adapter.py`
- Lines: 17

### `app\clean_catalog.py`
- Lines: 53
- Logs: app/logs/product_catalog.json, app/logs/product_performance.json

### `app\cleanup_forced_error.py`
- Lines: 13
- Runs steps: forced_test_error

### `app\cleanup_logs.py`
- Lines: 37

### `app\commerce\__init__.py`
- Lines: 0

### `app\commerce\routes.py`
- Lines: 146
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\commerce\routes_4_CHANNELS_CONNECTED_OK.py`
- Lines: 86

### `app\commerce\routes_6_CHANNELS_READY_OK.py`
- Lines: 145
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\commerce\routes_MULTI_CHANNEL_FINAL_OK.py`
- Lines: 145
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\commerce\routes_OVERVIEW_OK.py`
- Lines: 65

### `app\commerce\routes_REAL_OVERVIEW_OK.py`
- Lines: 98

### `app\commerce\routes_UNIQUE_TOTALS_OK.py`
- Lines: 96

### `app\compliance_layer.py`
- Lines: 76
- Functions: read_json
- Logs: app/logs/compliance_layer.json, app/logs/global_arbitrage_engine.json, app/logs/product_quality_filter.json

### `app\config.py`
- Lines: 21
- Classes: Settings, Config

### `app\connect_crm_smtp_draft.py`
- Lines: 26

### `app\control_panel.py`
- Lines: 19

### `app\conversion_watch.py`
- Lines: 50
- Logs: app/logs/conversion_watch.json, app/logs/imported_skus.json

### `app\core\config.py`
- Lines: 31
- Classes: Settings
- Functions: get_settings

### `app\crm_action_planner.py`
- Lines: 60
- Functions: read_json
- Logs: app/logs/crm_action_planner.json, app/logs/crm_automation_status.json, app/logs/customer_segmentation.json

### `app\crm_automation.py`
- Lines: 51
- Logs: app/logs/crm_automation_status.json

### `app\crm_channel_readiness.py`
- Lines: 76
- Logs: app/logs/crm_channel_readiness.json

### `app\crm_confirm_owner_for_test.py`
- Lines: 20
- Logs: app/logs/crm_send_guard.json

### `app\crm_draft_outbox.py`
- Lines: 40
- Functions: read_json
- Logs: app/logs/crm_channel_readiness.json, app/logs/crm_draft_outbox.json, app/logs/crm_message_generator.json, app/logs/crm_send_guard.json

### `app\crm_event_router.py`
- Lines: 58
- Functions: read_json
- Logs: app/logs/crm_draft_outbox.json, app/logs/crm_event_router.json, app/logs/real_sales_mode.json, app/logs/shopify_order_address_collector.json

### `app\crm_executor_dry_run.py`
- Lines: 43
- Functions: read_json
- Logs: app/logs/crm_channel_readiness.json, app/logs/crm_executor_dry_run.json, app/logs/crm_queue.json, app/logs/crm_send_guard.json

### `app\crm_final_gate.py`
- Lines: 38
- Functions: read_json
- Logs: app/logs/crm_final_gate.json, app/logs/crm_queue.json, app/logs/crm_readiness_summary.json, app/logs/crm_send_guard.json

### `app\crm_health_check.py`
- Lines: 43
- Functions: read_json
- Logs: app/logs/crm_automation_status.json, app/logs/crm_channel_readiness.json, app/logs/crm_health_check.json, app/logs/crm_message_generator.json, app/logs/crm_orchestrator.json, app/logs/crm_queue.json, app/logs/crm_send_guard.json

### `app\crm_message_generator.py`
- Lines: 43
- Logs: app/logs/crm_message_generator.json

### `app\crm_orchestrator.py`
- Lines: 39
- Functions: read_json
- Logs: app/logs/crm_channel_readiness.json, app/logs/crm_event_router.json, app/logs/crm_executor_dry_run.json, app/logs/crm_orchestrator.json, app/logs/crm_queue.json, app/logs/crm_send_guard.json

### `app\crm_personalized_drafts.py`
- Lines: 52
- Logs: app/logs/crm_personalized_drafts.json, app/logs/shopify_crm_events.json

### `app\crm_prepare_single_test.py`
- Lines: 32
- Logs: app/logs/crm_owner_confirmed.json, app/logs/crm_queue.json

### `app\crm_provider_config_check.py`
- Lines: 71
- Logs: app/logs/crm_provider_config_check.json

### `app\crm_queue_builder.py`
- Lines: 50
- Functions: read_json
- Logs: app/logs/crm_draft_outbox.json, app/logs/crm_event_router.json, app/logs/crm_queue.json, app/logs/crm_send_guard.json

### `app\crm_readiness_summary.py`
- Lines: 38
- Functions: read_json
- Logs: app/logs/crm_channel_readiness.json, app/logs/crm_health_check.json, app/logs/crm_queue.json, app/logs/crm_readiness_summary.json, app/logs/crm_send_guard.json, app/logs/smtp_config_validator.json

### `app\crm_send_one_test.py`
- Lines: 65
- ENV: SMTP_FROM_EMAIL, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER
- Logs: app/logs/crm_final_gate.json, app/logs/crm_queue.json, app/logs/crm_send_one_test.json

### `app\customer_analytics.py`
- Lines: 56
- Functions: read_json
- Logs: app/logs/customer_analytics.json, app/logs/real_sales_mode.json, app/logs/shopify_order_address_collector.json

### `app\customer_segmentation.py`
- Lines: 72
- Functions: read_json
- Logs: app/logs/customer_analytics.json, app/logs/customer_segmentation.json

### `app\daily_decision_report.py`
- Lines: 46
- Functions: load_json
- Logs: app/logs/conversion_watch.json, app/logs/disable_candidates.json, app/logs/pricing_experiments.json, app/logs/promotion_actions.json

### `app\daily_free_traffic_tasks.py`
- Lines: 18
- Logs: app/logs/social_post_plan.json

### `app\daily_report.py`
- Lines: 166
- Functions: read_json
- Logs: app/logs/daily_report.json, app/logs/external_blockers_monitor.json, app/logs/global_commerce_control_panel.json, app/logs/production_readiness_report.json, app/logs/real_sales_mode.json, app/logs/system_status_dashboard.json

### `app\daily_run.py`
- Lines: 36

### `app\daily_summary.py`
- Lines: 49
- Logs: app/logs/autopilot_priority_queue.json, app/logs/autopilot_run.json, app/logs/product_performance.json

### `app\db.py`
- Lines: 15
- ENV: DATABASE_URL

### `app\debug_pipeline.py`
- Lines: 18
- Logs: app/logs/hunter_promoted.json, app/logs/imported_skus.json

### `app\decision_engine.py`
- Lines: 70
- Logs: app/logs/autopilot_decisions.json, app/logs/product_performance.json

### `app\deployment_readiness_checklist.py`
- Lines: 77
- Functions: read_json
- Logs: app/logs/crm_final_gate.json, app/logs/deployment_readiness_checklist.json, app/logs/master_system_health.json, app/logs/niche_exclusion_summary.json, app/logs/smtp_config_validator.json, app/logs/supplier_fallback_engine.json, app/logs/system_status_dashboard.json

### `app\deployment_summary.py`
- Lines: 37
- Functions: read_json
- Logs: app/logs/deployment_readiness_checklist.json, app/logs/deployment_summary.json, app/logs/master_system_health.json, app/logs/system_release_marker.json

### `app\disable_candidates.py`
- Lines: 40
- Logs: app/logs/disable_candidates.json, app/logs/imported_skus.json

### `app\download_dog_socks_image.py`
- Lines: 14

### `app\download_product_images.py`
- Lines: 37

### `app\dynamic_product_score.py`
- Lines: 90
- Logs: app/logs/dynamic_product_score.json, app/logs/imported_skus.json

### `app\dynamic_score_sync.py`
- Lines: 65
- Logs: app/logs/dynamic_product_score.json, app/logs/dynamic_score_sync.json, app/logs/imported_skus.json

### `app\emergency_stop_validator.py`
- Lines: 30
- Logs: app/logs/auto_spend_executor.json, app/logs/emergency_stop_validator.json, app/logs/hourly_budget_monitor.json

### `app\enable_crm_limited_send.py`
- Lines: 24

### `app\engines\__init__.py`
- Lines: 0

### `app\engines\action_executor.py`
- Lines: 32

### `app\engines\automation_daemon_worker.py`
- Lines: 80

### `app\engines\automation_log.py`
- Lines: 24

### `app\engines\automation_rules.py`
- Lines: 69

### `app\engines\automation_ruleset_loader.py`
- Lines: 37

### `app\engines\automation_state.py`
- Lines: 39

### `app\engines\automation_tick.py`
- Lines: 55

### `app\engines\compliance.py`
- Lines: 78

### `app\engines\daemon_restore.py`
- Lines: 39

### `app\engines\decision_logger.py`
- Lines: 31

### `app\engines\decision_memory.py`
- Lines: 112

### `app\engines\demand.py`
- Lines: 80

### `app\engines\executor.py`
- Lines: 93

### `app\engines\global_commerce_brain.py`
- Lines: 439

### `app\engines\marketplace.py`
- Lines: 85
- Functions: build_marketplace_intelligence

### `app\engines\marketplace_scoring.py`
- Lines: 99

### `app\engines\product_lookup.py`
- Lines: 12

### `app\engines\queue.py`
- Lines: 52

### `app\engines\routing.py`
- Lines: 108

### `app\engines\rule_engine.py`
- Lines: 50

### `app\engines\seo.py`
- Lines: 81

### `app\engines\wallet_engine.py`
- Lines: 271

### `app\env_manager.py`
- Lines: 33
- Functions: load_local_env, get_env, env_file_exists

### `app\event_collector_state.py`
- Lines: 25
- Logs: app/logs/event_collector_state.json

### `app\event_learning_sync.py`
- Lines: 21
- Logs: app/logs/event_collector_state.json, app/logs/meta_test_event.json

### `app\example.py`
- Lines: 2

### `app\expand_catalog.py`
- Lines: 44
- Logs: app/logs/product_catalog.json

### `app\exploration_engine.py`
- Lines: 33
- Logs: app/logs/autopilot_decisions.json, app/logs/exploration_candidates.json

### `app\exploration_engine_v2.py`
- Lines: 94
- Logs: app/logs/exploration_v2.json, app/logs/product_performance.json

### `app\external_blockers_monitor.py`
- Lines: 127
- Functions: read_json
- Logs: app/logs/external_blockers_monitor.json, app/logs/external_platform_blockers.json, app/logs/global_commerce_control_panel.json, app/logs/production_readiness_report.json

### `app\external_platform_blockers.py`
- Lines: 74
- Functions: load
- Logs: app/logs/external_platform_blockers.json, app/logs/google_campaign_live_result.json, app/logs/meta_campaign_live_result.json, app/logs/meta_campaign_registry.json

### `app\feeds\__init__.py`
- Lines: 0

### `app\final_mvp\__init__.py`
- Lines: 1

### `app\final_mvp\db.py`
- Lines: 50
- Classes: Opportunity, AutonomousEvent
- Functions: init_db, db_status
- ENV: DATABASE_URL

### `app\final_mvp\governor.py`
- Lines: 38
- Classes: Governor
- Functions: _float, _bool, status, allow_action

### `app\final_mvp\product_pipeline.py`
- Lines: 54
- Classes: SupplierItem, ProductFinder
- Functions: __init__, find

### `app\final_mvp\routes.py`
- Lines: 97
- Classes: ShopifyDraftRequest
- Functions: status, database_status, run_opportunities, stop_worker, events

### `app\final_mvp\scoring.py`
- Lines: 48
- Functions: score_item

### `app\final_mvp\worker.py`
- Lines: 81
- Classes: WorkerState
- Functions: dict
- ENV: AUTONOMOUS_INTERVAL_SECONDS, MAX_PRODUCTS_PER_CYCLE

### `app\final_system_check.py`
- Lines: 74
- Functions: load_json
- Logs: app/logs/blocked_products.json, app/logs/conversion_watch.json, app/logs/imported_skus.json, app/logs/pricing_experiments.json, app/logs/promotion_actions.json, app/logs/promotion_candidates.json

### `app\final_system_checkpoint.py`
- Lines: 36
- Logs: app/logs/final_system_checkpoint.json, app/logs/system_health_dashboard.json

### `app\finance\__init__.py`
- Lines: 0

### `app\finance\schemas.py`
- Lines: 78
- Classes: FeeModel, CostAssumptions, AdvancedProfitBreakdown, ProfitScenario, ScenarioResult, AdvancedEvaluationRequest
- Functions: uppercase_currency

### `app\fix_bom_campaign_queue.py`
- Lines: 12

### `app\fix_error_handler.py`
- Lines: 13

### `app\fix_unicode_report.py`
- Lines: 10

### `app\fulfillment\__init__.py`
- Lines: 0

### `app\fulfillment\schemas.py`
- Lines: 61
- Classes: FulfillmentStatus, ShippingAddress, FulfillmentRequest, FulfillmentResult
- Functions: normalize_currency

### `app\fulfillment\service.py`
- Lines: 120
- Classes: FulfillmentService
- Functions: __init__

### `app\fulfillment_status_report.py`
- Lines: 40
- Functions: load
- Logs: app/logs/cj_purchase_attempts.json, app/logs/fulfillment_status_report.json, app/logs/incoming_orders.json, app/logs/supplier_purchase_queue.json, app/logs/tracking_updates.json

### `app\full_system_final_run.py`
- Lines: 78
- Logs: app/logs/full_system_final_run.json

### `app\generate_product_images.py`
- Lines: 19

### `app\global_arbitrage_engine.py`
- Lines: 47
- Logs: app/logs/opportunities/global_arbitrage_report.json, app/logs/opportunities/opportunity_report.json

### `app\global_channel_requirements_check.py`
- Lines: 66
- Logs: app/logs/global_channel_requirements_check.json

### `app\global_channel_status_summary.py`
- Lines: 49
- Functions: read_json
- Logs: app/logs/global_channel_requirements_check.json, app/logs/global_channel_status_summary.json, app/logs/global_marketplace_roadmap.json

### `app\global_commerce_control_panel.py`
- Lines: 62
- Functions: load, platform_status
- Logs: app/logs/ad_campaign_executor.json, app/logs/external_platform_blockers.json, app/logs/final_system_checkpoint.json, app/logs/global_commerce_control_panel.json, app/logs/meta_launch_readiness.json, app/logs/opportunities/global_execution_plan.json, app/logs/real_sales_mode.json, app/logs/supplier_purchase_executor.json

### `app\global_execution_plan.py`
- Lines: 54
- Logs: app/logs/opportunities/global_arbitrage_report.json, app/logs/opportunities/global_execution_limits.json, app/logs/opportunities/global_execution_plan.json

### `app\global_marketplace_roadmap.py`
- Lines: 110
- Logs: app/logs/global_marketplace_roadmap.json

### `app\health_check.py`
- Lines: 41
- ENV: DRY_RUN, IMPORT_EXISTING_ACTION, SHOPIFY_ACCESS_TOKEN, SHOPIFY_STORE_URL, SUPPLIER_API_URL, SUPPLIER_MODE

### `app\hourly_budget_monitor.py`
- Lines: 35
- Logs: app/logs/auto_spend_executor.json, app/logs/hourly_budget_monitor.json

### `app\hunter_action_executor.py`
- Lines: 57
- Logs: app/logs/hunter_action_execution.json, app/logs/hunter_action_plan.json, app/logs/imported_skus.json

### `app\hunter_action_plan.py`
- Lines: 39
- Logs: app/logs/hunter_action_plan.json, app/logs/imported_skus.json

### `app\hunter_import.py`
- Lines: 36
- Logs: app/logs/hunter_promoted.json, app/logs/imported_skus.json

### `app\hunter_registry_sync.py`
- Lines: 93
- Logs: app/logs/hunter_feedback.json, app/logs/hunter_registry_sync.json, app/logs/imported_skus.json

### `app\import_report.py`
- Lines: 23

### `app\insert_winner_notify.py`
- Lines: 29

### `app\listings\__init__.py`
- Lines: 0

### `app\listings\generator.py`
- Lines: 123
- Classes: MarketplaceRules, AutoListingGenerator
- Functions: generate, _build_title, _build_bullets, _build_description, _build_keywords, _quality_check, _clean_text, _truncate_words

### `app\listings\schemas.py`
- Lines: 40
- Classes: ListingTone, MarketplaceFormat, ListingGenerationRequest, ListingQualityCheck, GeneratedListing

### `app\live_api_execution_gate.py`
- Lines: 44
- Logs: app/logs/live_api_execution_gate.json, app/logs/live_campaign_registry.json, app/logs/live_spend_permission_gate.json

### `app\live_backend_router.py`
- Lines: 32
- Logs: app/logs/live_backend_router.json, app/logs/live_spend_permission_gate.json

### `app\live_campaign_registry.py`
- Lines: 49
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/live_campaign_registry.json, app/logs/meta_live_campaign_payloads.json

### `app\live_execution_consolidator.py`
- Lines: 51
- Logs: app/logs/google_live_execution_result.json, app/logs/live_execution_consolidated.json, app/logs/meta_live_execution_result.json

### `app\live_execution_reporter.py`
- Lines: 50
- Logs: app/logs/live_api_execution_gate.json, app/logs/live_execution_report.json

### `app\live_mode_final_lock.py`
- Lines: 33
- Logs: app/logs/live_execution_report.json, app/logs/live_mode_final_lock.json

### `app\live_spend_audit_ledger.py`
- Lines: 29
- Logs: app/logs/live_execution_consolidated.json, app/logs/live_spend_audit_ledger.jsonl

### `app\live_spend_audit_reader.py`
- Lines: 22
- Logs: app/logs/live_spend_audit_ledger.jsonl

### `app\live_spend_permission_gate.py`
- Lines: 38
- Logs: app/logs/auto_spend_executor.json, app/logs/emergency_stop_validator.json, app/logs/live_spend_permission_gate.json

### `app\main.py`
- Lines: 2755
- Functions: get_working_shopify_token, load_env_local, ensure_runtime_env_file, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status
- ENV: ADS_ENABLED, AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, AUTO_PUBLISH_ENABLED, CJ_ACCESS_TOKEN, DRY_RUN, EMERGENCY_STOP, GOOGLE_ADS_ENABLED, MAX_DAILY_AD_SPEND, META_ACCESS_TOKEN, META_ADS_ENABLED, META_AD_ACCOUNT_ID, META_PIXEL_ID, MIN_MARGIN_PERCENT
- Logs: app/logs/imported_skus.json

### `app\main_CATALOG_HEALTH_OK.py`
- Lines: 1888
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_CLEAN_CATALOG_OK.py`
- Lines: 1822
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_SAFE_FLOW_OK.py`
- Lines: 1853
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_WORKING_DEDUPE_OK.py`
- Lines: 1796
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_backup.py`
- Lines: 1570
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY, SUPPLIER_MODE
- Logs: app/logs/imported_skus.json

### `app\main_broken_20260518_112242.py`
- Lines: 1570
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY, SUPPLIER_MODE
- Logs: app/logs/imported_skus.json

### `app\main_restored.py`
- Lines: 19

### `app\mark_manual_social_posts.py`
- Lines: 15
- Logs: app/logs/manual_social_publish_log.json

### `app\market_arbitrage_engine.py`
- Lines: 89
- Logs: app/logs/imported_skus.json, app/logs/market_arbitrage_candidates.json

### `app\marketplaces\__init__.py`
- Lines: 4

### `app\marketplaces\base.py`
- Lines: 37
- Classes: MarketplaceClient
- Functions: name

### `app\marketplaces\mock_marketplace.py`
- Lines: 86
- Classes: MockMarketplaceClient
- Functions: name

### `app\marketplaces\registry.py`
- Lines: 24
- Classes: MarketplaceRegistry
- Functions: __init__, get, list_names

### `app\marketplaces\schemas.py`
- Lines: 75
- Classes: MarketplaceName, ListingStatus, MarketplaceFees, ListingDraft, ListingResult, MarketplaceOrder, PriceUpdateRequest
- Functions: uppercase_currency, uppercase_currency

### `app\master_system_health.py`
- Lines: 70
- Functions: read_json
- Logs: app/logs/alerts.json, app/logs/backup_report.json, app/logs/budget_controller.json, app/logs/compliance_layer.json, app/logs/crm_final_gate.json, app/logs/inventory_sync_guard.json, app/logs/master_system_health.json, app/logs/niche_exclusion_summary.json, app/logs/product_quality_filter.json, app/logs/recovery_report.json, app/logs/roi_engine.json, app/logs/supplier_fallback_engine.json, app/logs/system_status_dashboard.json

### `app\models.py`
- Lines: 15

### `app\multi_market_scanner.py`
- Lines: 65
- Logs: app/logs/global_arbitrage_candidates.json

### `app\niche_exclusion_registry.py`
- Lines: 42
- Logs: app/logs/niche_exclusion_registry.json

### `app\niche_exclusion_summary.py`
- Lines: 31
- Functions: read_json
- Logs: app/logs/niche_exclusion_guard.json, app/logs/niche_exclusion_registry.json, app/logs/niche_exclusion_summary.json, app/logs/pet_niche_filter.json

### `app\no_sales_report.py`
- Lines: 31
- Logs: app/logs/imported_skus.json, app/logs/no_sales_report.json

### `app\oauth_reauth_required.py`
- Lines: 56
- Logs: app/logs/oauth_reauth_required.json, app/logs/token_manager_status.json

### `app\opportunity_engine.py`
- Lines: 51
- Logs: app/logs/opportunities/margin_report.json, app/logs/opportunities/opportunity_report.json

### `app\organic_money_launch_plan.py`
- Lines: 38
- Logs: app/logs/organic_money_launch_plan.json

### `app\paid_ads_status.py`
- Lines: 39
- Logs: app/logs/google_ads_readiness.json, app/logs/meta_ads_readiness.json, app/logs/paid_ads_status.json

### `app\patch_alert_import.py`
- Lines: 16

### `app\patch_auto_scaling_alerts.py`
- Lines: 39

### `app\patch_campaign_alert_dispatcher.py`
- Lines: 32

### `app\patch_campaign_approval_queue.py`
- Lines: 15
- Runs steps: campaign_approval_queue, campaign_hub

### `app\patch_campaign_hub.py`
- Lines: 15
- Runs steps: campaign_hub, google_ad_drafts_from_content

### `app\patch_campaign_queue_alerts.py`
- Lines: 43

### `app\patch_ceo_alert.py`
- Lines: 32

### `app\patch_daily_summary_priority.py`
- Lines: 31
- Logs: app/logs/autopilot_priority_queue.json

### `app\patch_error_hook.py`
- Lines: 28

### `app\patch_report_enhancer.py`
- Lines: 16

### `app\patch_report_exploration_v2.py`
- Lines: 37
- Logs: app/logs/exploration_v2.json

### `app\patch_scale_alerts.py`
- Lines: 32

### `app\patch_send_daily_summary.py`
- Lines: 16
- Runs steps: daily_summary, send_daily_summary

### `app\patch_social_content_enhancer.py`
- Lines: 14
- Runs steps: social_content_enhancer, social_content_generator

### `app\patch_social_content_generator.py`
- Lines: 14
- Runs steps: action_executor, social_content_generator

### `app\patch_status_action_executor.py`
- Lines: 25
- Logs: app/logs/action_executor.json

### `app\patch_system_alerts.py`
- Lines: 28

### `app\patch_telegram_summary.py`
- Lines: 15
- Runs steps: send_daily_summary, send_telegram_summary

### `app\patch_winner_alert.py`
- Lines: 28

### `app\patch_winner_log.py`
- Lines: 20

### `app\patch_winner_protection.py`
- Lines: 23

### `app\performance_board.py`
- Lines: 49
- Logs: app/logs/imported_skus.json, app/logs/performance_board.json

### `app\pet_niche_filter.py`
- Lines: 92
- Functions: read_json
- Logs: app/logs/pet_niche_filter.json, app/logs/registry_quality_report.json, app/logs/shopify_registry_hydrator.json

### `app\pipeline_summary.py`
- Lines: 31
- Logs: app/logs/imported_skus.json

### `app\product_hunter\__init__.py`
- Lines: 0

### `app\product_hunter\demand.py`
- Lines: 61
- Classes: DemandEstimator
- Functions: estimate, aggregate, _title_intent_score, _market_fit_score

### `app\product_hunter\mapper.py`
- Lines: 61
- Functions: map_category, supplier_product_to_candidate

### `app\product_hunter\schemas.py`
- Lines: 56
- Classes: OpportunityStatus, DemandSignal, HunterRequest, ProductOpportunity, HunterResponse
- Functions: uppercase_currency

### `app\product_hunter\scoring.py`
- Lines: 38
- Classes: OpportunityScorer
- Functions: score, _aggregate, _decision_factor

### `app\product_hunter\service.py`
- Lines: 140
- Classes: ProductHunterService
- Functions: __init__, _evaluate_supplier_product, _estimate_competition, _recommended_sale_price, _explain
- Logs: app/logs/hunter_promoted.json

### `app\product_image_sync_status.py`
- Lines: 28
- Logs: app/logs/local_product_images.json, app/logs/product_image_sync_status.json

### `app\product_quality_filter.py`
- Lines: 80
- Functions: read_json
- Logs: app/logs/dynamic_product_score.json, app/logs/global_arbitrage_engine.json, app/logs/product_quality_filter.json, app/logs/tier_summary.json

### `app\production\__init__.py`
- Lines: 1

### `app\production\logging_config.py`
- Lines: 24
- Functions: configure_logging, get_logger
- ENV: LOG_LEVEL

### `app\production\routes.py`
- Lines: 45
- Functions: production_status, health, config_check, check_safety, log_test

### `app\production\settings.py`
- Lines: 46
- Classes: ProductionSettings
- Functions: bool_env, float_env, get_production_settings
- ENV: APP_ENV, DATABASE_URL, OPENAI_API_KEY, SHIPPING_MODE, SHOPIFY_ACCESS_TOKEN, SHOPIFY_STORE_URL, SUPPLIER_MODE

### `app\production_readiness_report.py`
- Lines: 39
- Functions: load
- Logs: app/logs/final_system_checkpoint.json, app/logs/global_commerce_control_panel.json, app/logs/meta_activation_executor.json, app/logs/meta_auto_stop_monitor.json, app/logs/meta_launch_readiness.json, app/logs/production_readiness_report.json

### `app\promotion_actions.py`
- Lines: 46
- Logs: app/logs/promotion_actions.json, app/logs/promotion_candidates.json

### `app\promotion_candidates.py`
- Lines: 44
- Logs: app/logs/imported_skus.json, app/logs/promotion_candidates.json

### `app\promotion_plan.py`
- Lines: 35
- Logs: app/logs/promotion_actions.json

### `app\quick_status.py`
- Lines: 40
- Functions: read_json
- Logs: app/logs/alerts.json, app/logs/crm_final_gate.json, app/logs/global_channel_status_summary.json, app/logs/master_system_health.json, app/logs/niche_exclusion_summary.json, app/logs/smtp_config_validator.json, app/logs/system_status_dashboard.json

### `app\real_sales_collector.py`
- Lines: 201
- Functions: load_env, norm_shop, add_sale
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_OAUTH_TOKEN, EBAY_USER_TOKEN, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET, WC_STORE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, WOO_STORE_URL
- Logs: app/logs/imported_skus.json, app/logs/real_sales_report.json

### `app\real_sales_loop_status.py`
- Lines: 64
- Functions: read_json
- Logs: app/logs/autonomous_order_router.json, app/logs/cj_customer_address_validator.json, app/logs/cj_order_drafts.json, app/logs/cj_order_payloads.json, app/logs/cj_supplier_readiness.json, app/logs/real_sales_loop_status.json, app/logs/real_sales_mode.json, app/logs/shopify_order_address_collector.json

### `app\real_sales_mode.py`
- Lines: 23
- Logs: app/logs/real_sales_mode.json, app/logs/real_sales_report_filtered.json

### `app\real_traffic_launcher.py`
- Lines: 36
- Logs: app/logs/opportunities/global_execution_plan.json, app/logs/real_traffic_launcher.json

### `app\recovery_layer.py`
- Lines: 75
- Functions: read_json, compare
- Logs: app/logs/last_known_good_state.json, app/logs/recovery_report.json, app/logs/system_status_dashboard.json

### `app\refund_dispute_engine.py`
- Lines: 48
- Logs: app/logs/refund_dispute_engine.json

### `app\registry_inspector.py`
- Lines: 16
- Logs: app/logs/imported_skus.json

### `app\registry_push_sync.py`
- Lines: 37
- Logs: app/logs/imported_skus.json, app/logs/seo_mass_push_execution.json

### `app\registry_quality_report.py`
- Lines: 37
- Logs: app/logs/imported_skus.json, app/logs/registry_quality_report.json

### `app\release_checklist.py`
- Lines: 29
- ENV: DRY_RUN, SHOPIFY_ACCESS_TOKEN, SHOPIFY_STORE_URL, SUPPLIER_API_KEY, SUPPLIER_MODE

### `app\release_history.py`
- Lines: 39
- Functions: read_json
- Logs: app/logs/release_history.json, app/logs/system_release_marker.json

### `app\restore_performance.py`
- Lines: 44
- Logs: app/logs/product_performance.json

### `app\risk\__init__.py`
- Lines: 0

### `app\risk\advanced_risk_engine.py`
- Lines: 56
- Classes: AdvancedRiskEngine
- Functions: evaluate

### `app\risk\schemas.py`
- Lines: 18
- Classes: RiskSignal, AdvancedRiskReport

### `app\routes\upgrade_routes.py`
- Lines: 60
- Classes: ScoreRequest
- Functions: upgrade_status, score_product, start_worker, stop_worker, supplier_search, shopify_status

### `app\run_all.py`
- Lines: 13

### `app\run_lock.py`
- Lines: 28

### `app\sales_cleanup.py`
- Lines: 46
- Logs: app/logs/real_sales_report.json, app/logs/real_sales_report_filtered.json

### `app\sales_mode.py`
- Lines: 25
- Logs: app/logs/sales_mode.json

### `app\save_last_known_good_state.py`
- Lines: 27
- Logs: app/logs/last_known_good_state.json, app/logs/system_status_dashboard.json

### `app\scale_plan.py`
- Lines: 32
- Logs: app/logs/performance_board.json, app/logs/scale_plan.json

### `app\scale_plan_v2.py`
- Lines: 52
- Logs: app/logs/scale_plan.json, app/logs/scale_plan_v2.json

### `app\scheduled_import.py`
- Lines: 23

### `app\schemas\decision.py`
- Lines: 41
- Classes: DecisionStatus, ProfitBreakdown, CommerceDecision, AdvancedCommerceDecision

### `app\schemas\product.py`
- Lines: 44
- Classes: ProductCategory, SupplierOffer, ProductCandidate
- Functions: uppercase_currency

### `app\send_daily_summary.py`
- Lines: 58
- ENV: OWNER_EMAIL, SMTP_FROM_EMAIL, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER
- Logs: app/logs/send_daily_summary.json

### `app\send_telegram_alert.py`
- Lines: 29
- ENV: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

### `app\send_telegram_summary.py`
- Lines: 60
- ENV: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
- Logs: app/logs/send_telegram_summary.json

### `app\seo_action_report.py`
- Lines: 47
- Logs: app/logs/imported_skus.json, app/logs/promotion_candidates.json, app/logs/seo_action_report.json

### `app\seo_auto_apply.py`
- Lines: 88
- Logs: app/logs/imported_skus.json, app/logs/seo_auto_apply_results.json, app/logs/traffic_execution_plan.json

### `app\seo_cleaner.py`
- Lines: 53
- Logs: app/logs/traffic_execution_plan_clean.json, app/logs/traffic_execution_plan_full.json

### `app\seo_finalizer.py`
- Lines: 52
- Logs: app/logs/traffic_execution_plan_clean.json, app/logs/traffic_execution_plan_final.json

### `app\seo_generate_full.py`
- Lines: 42
- Logs: app/logs/imported_skus.json, app/logs/traffic_execution_plan_full.json

### `app\seo_mass_apply.py`
- Lines: 55
- Logs: app/logs/imported_skus.json, app/logs/seo_mass_apply_results.json, app/logs/traffic_execution_plan_final.json

### `app\seo_mass_push_executor.py`
- Lines: 84
- Logs: app/logs/seo_mass_push_execution.json, app/logs/seo_mass_push_plan_final.json, app/logs/seo_push_summary.json

### `app\seo_mass_push_plan.py`
- Lines: 49
- Logs: app/logs/imported_skus.json, app/logs/seo_mass_push_plan.json

### `app\seo_optimizer.py`
- Lines: 99
- Functions: clean_title, ebay_title, shopify_title, bullet_points, seo_tags

### `app\seo_pipeline_audit.py`
- Lines: 56
- Logs: app/logs/imported_skus.json, app/logs/seo_pipeline_audit.json

### `app\seo_push_executor.py`
- Lines: 53
- Logs: app/logs/seo_push_plan.json, app/logs/seo_push_results.json

### `app\seo_push_to_channels.py`
- Lines: 47
- Logs: app/logs/imported_skus.json, app/logs/seo_push_plan.json

### `app\seo_quality_fix.py`
- Lines: 74
- Logs: app/logs/imported_skus.json, app/logs/seo_quality_fix_results.json

### `app\seo_quality_score.py`
- Lines: 64
- Logs: app/logs/imported_skus.json, app/logs/seo_quality_report.json

### `app\seo_report.py`
- Lines: 41

### `app\seo_repush_executor.py`
- Lines: 27
- Logs: app/logs/seo_repush_execution.json, app/logs/seo_repush_required.json

### `app\seo_repush_required.py`
- Lines: 24
- Logs: app/logs/imported_skus.json, app/logs/seo_repush_required.json

### `app\seo_suggestions.py`
- Lines: 38
- Logs: app/logs/seo_action_report.json, app/logs/seo_suggestions.json

### `app\services\advanced_governor.py`
- Lines: 69
- Classes: AdvancedAIGovernor
- Functions: __init__, evaluate

### `app\services\audit.py`
- Lines: 15
- Classes: AuditLogger
- Functions: log, all

### `app\services\fulfillment_agent.py`
- Lines: 10
- Classes: FulfillmentAgent
- Functions: create_supplier_order

### `app\services\governor.py`
- Lines: 63
- Classes: AIGovernor
- Functions: __init__, evaluate

### `app\services\risk_engine.py`
- Lines: 19
- Classes: RiskEngine
- Functions: score

### `app\shipping\__init__.py`
- Lines: 4

### `app\shipping\base.py`
- Lines: 18
- Classes: ShippingCarrier

### `app\shipping\mock_carriers.py`
- Lines: 82
- Classes: DeterministicMockCarrier, RoyalMailMockCarrier, EvriMockCarrier, DHLMockCarrier
- Functions: __init__, __init__, __init__, __init__

### `app\shipping\registry.py`
- Lines: 36
- Classes: ShippingRegistry
- Functions: __init__, list_names, get

### `app\shipping\schemas.py`
- Lines: 74
- Classes: CarrierName, Address, Parcel, ShippingRateRequest, ShippingRate, ShipmentRequest, Shipment, TrackingEvent

### `app\shipping\selector.py`
- Lines: 12
- Classes: ShippingSelector
- Functions: choose_best

### `app\shopify_automation\__init__.py`
- Lines: 1

### `app\shopify_automation\analytics.py`
- Lines: 48
- Functions: calculate_store_kpis

### `app\shopify_automation\duplicate_fix.py`
- Lines: 24
- Functions: detect_duplicate_skus

### `app\shopify_automation\routes.py`
- Lines: 580
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog, orders_sync, orders_summary, shopify_automation_dashboard
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\shopify_automation\routes_ACTIONS_OK.py`
- Lines: 580
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog, orders_sync, orders_summary, shopify_automation_dashboard
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\shopify_automation\routes_WORKING_OK.py`
- Lines: 559
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog, orders_sync, orders_summary, shopify_automation_dashboard
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\shopify_automation\rules.py`
- Lines: 87
- Functions: normalize_product, evaluate_auto_publish, detect_duplicate_skus

### `app\shopify_automation\rules_OK.py`
- Lines: 87
- Functions: normalize_product, evaluate_auto_publish, detect_duplicate_skus

### `app\show_routes.py`
- Lines: 4

### `app\simulate_click.py`
- Lines: 26
- Logs: app/logs/manual_channel_metrics.json

### `app\smtp_config_validator.py`
- Lines: 49
- ENV: SMTP_FROM_EMAIL, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER
- Logs: app/logs/smtp_config_validator.json

### `app\social_content_enhancer.py`
- Lines: 76
- Logs: app/logs/social_content_enhanced.json, app/logs/social_content_plan.json

### `app\social_content_generator.py`
- Lines: 36
- Logs: app/logs/publish_execution_plan.json, app/logs/social_content_plan.json

### `app\social_post_plan.py`
- Lines: 42
- Logs: app/logs/social_post_plan.json

### `app\spend_history_tracker.py`
- Lines: 57
- Logs: app/logs/auto_spend_executor.json, app/logs/spend_history_tracker.json

### `app\stable_release_105.py`
- Lines: 42
- Functions: read_json
- Logs: app/logs/master_system_health.json, app/logs/operator_runbook.json, app/logs/stable_release_105.json, app/logs/system_status_dashboard.json

### `app\status_report.py`
- Lines: 36
- ENV: DRY_RUN, SHOPIFY_ACCESS_TOKEN, SUPPLIER_MODE

### `app\stock_report.py`
- Lines: 25

### `app\suppliers\__init__.py`
- Lines: 4

### `app\suppliers\ai_product_score.py`
- Lines: 58
- Functions: score_product

### `app\suppliers\audit_log.py`
- Lines: 19

### `app\suppliers\base.py`
- Lines: 31
- Classes: SupplierClient

### `app\suppliers\blocked_log.py`
- Lines: 31

### `app\suppliers\currency.py`
- Lines: 30
- Classes: CurrencyConverter
- Functions: __init__, convert

### `app\suppliers\import_state.py`
- Lines: 30

### `app\suppliers\normalize_product.py`
- Lines: 56
- Functions: _first_price, normalize_supplier_product

### `app\suppliers\normalizer.py`
- Lines: 53
- Classes: SupplierNormalizer
- Functions: __init__, to_offer, category, _supplier_risk

### `app\suppliers\registry.py`
- Lines: 31
- Classes: SupplierRegistry
- Functions: __init__, register

### `app\suppliers\schemas.py`
- Lines: 70
- Classes: SupplierCapability, Money, SupplierProduct, SupplierSearchQuery, SupplierOrderRequest, SupplierOrderResult
- Functions: normalize_currency, normalize_currency

### `app\suppliers\seo_mapper.py`
- Lines: 33

### `app\suppliers\stock_state.py`
- Lines: 46

### `app\suppliers\title_optimizer.py`
- Lines: 22

### `app\support\__init__.py`
- Lines: 1

### `app\support\schemas.py`
- Lines: 82
- Classes: SupportIntent, SupportTone, EscalationReason, SupportMessage, SupportContext, SupportRequest, SupportClassification, SupportReply
- Functions: normalize_language

### `app\support\service.py`
- Lines: 179
- Classes: CustomerSupportAI
- Functions: classify, draft_reply, _sentiment_score, _greeting, _subject, _body_for_intent, _next_actions

### `app\sync_catalog_performance.py`
- Lines: 27
- Logs: app/logs/product_catalog.json, app/logs/product_performance.json

### `app\system_maintenance_planner.py`
- Lines: 45
- Logs: app/logs/system_maintenance_planner.json

### `app\system_release_marker.py`
- Lines: 48
- Functions: read_json
- Logs: app/logs/master_system_health.json, app/logs/niche_exclusion_summary.json, app/logs/system_release_marker.json, app/logs/system_status_dashboard.json

### `app\system_status_report.py`
- Lines: 94
- Functions: read_json
- Logs: app/logs/action_executor.json, app/logs/amazon_connection_status.json, app/logs/autopilot_priority_queue.json, app/logs/autopilot_run.json, app/logs/crm_readiness_summary.json, app/logs/etsy_autopilot.json, app/logs/etsy_connection_status.json, app/logs/google_campaign_live_creator.json, app/logs/master_system_health.json, app/logs/meta_launch_readiness.json

### `app\telegram_test.py`
- Lines: 27
- ENV: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

### `app\temu_scanner.py`
- Lines: 0

### `app\tier_strategy_apply.py`
- Lines: 45
- Logs: app/logs/imported_skus.json

### `app\tier_summary.py`
- Lines: 66
- Logs: app/logs/imported_skus.json, app/logs/tier_summary.json

### `app\tiktok_connection_status.py`
- Lines: 54
- Logs: app/logs/tiktok_connection_status.json

### `app\tiktok_trend_scanner.py`
- Lines: 0

### `app\token_manager.py`
- Lines: 419
- Functions: now, load_env, save_env_var, shop_domain, row
- ENV: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN, META_ACCESS_TOKEN, META_APP_ID, META_APP_SECRET, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP, SHOPIFY_STORE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET, WC_STORE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET
- Logs: app/logs/token_manager_status.json

### `app\traffic_brain.py`
- Lines: 88
- Logs: app/logs/arbitrage_safety_gate.json, app/logs/promotion_candidates.json, app/logs/traffic_candidates.json

### `app\traffic_execution_plan.py`
- Lines: 80
- Logs: app/logs/pricing_experiments.json, app/logs/seo_suggestions.json, app/logs/traffic_candidates.json, app/logs/traffic_execution_plan.json

### `app\traffic_mode.py`
- Lines: 47
- Logs: app/logs/event_collector_state.json, app/logs/paid_ads_status.json, app/logs/traffic_mode.json

### `app\traffic_prelaunch.py`
- Lines: 25
- Logs: app/logs/traffic_prelaunch.json

### `app\traffic_priority_plan.py`
- Lines: 50
- Logs: app/logs/channel_performance.json, app/logs/traffic_priority_plan.json

### `app\traffic_readiness.py`
- Lines: 31
- Logs: app/logs/paid_ads_status.json, app/logs/real_sales_mode.json, app/logs/traffic_mode.json, app/logs/traffic_readiness.json

### `app\update_product_performance.py`
- Lines: 34
- Logs: app/logs/product_performance.json

### `app\upgrade\__init__.py`
- Lines: 1

### `app\upgrade\ai_scoring.py`
- Lines: 65
- Classes: ProductOpportunityInput, ProductOpportunityScore
- Functions: score_product_opportunity

### `app\upgrade\background_worker.py`
- Lines: 14

### `app\upgrade\database.py`
- Lines: 18
- Functions: database_status
- ENV: DATABASE_URL

### `app\upgrade\risk_governor.py`
- Lines: 37
- Classes: RiskDecision
- Functions: env_float, is_emergency_stop, check_trade_allowed
- ENV: AUTONOMY_ENABLED, DRY_RUN, EMERGENCY_STOP

### `app\upgrade\worker_state.py`
- Lines: 20
- Classes: WorkerState
- Functions: to_dict, mark_cycle

### `app\utm_social_links.py`
- Lines: 64
- Logs: app/logs/utm_social_links.json

### `clean_mock_logs.py`
- Lines: 35
- Logs: app/logs/blocked_products.json, app/logs/image_failed_skus.json, app/logs/imported_skus.json, app/logs/stock_state.json

### `fix_ai_product_score.py`
- Lines: 66

### `fix_catalog_sku.py`
- Lines: 24

### `fix_final_routes.py`
- Lines: 34

### `fix_logging_no_jsonlogger.py`
- Lines: 38
- ENV: LOG_LEVEL

### `fix_production_routes.py`
- Lines: 34

### `patch_ai_score.py`
- Lines: 37

### `patch_ai_score_category.py`
- Lines: 36

### `patch_auto_disable_not_imported.py`
- Lines: 12

### `patch_auto_disable_score.py`
- Lines: 18

### `patch_daily_run_reports.py`
- Lines: 10

### `patch_disable_sandbox.py`
- Lines: 16

### `patch_hunter_promote.py`
- Lines: 45

### `patch_hunter_relax.py`
- Lines: 14

### `patch_hunter_request_schema.py`
- Lines: 17

### `patch_hunter_save.py`
- Lines: 32
- Logs: app/logs/hunter_promoted.json

### `patch_hunter_sku.py`
- Lines: 13

### `patch_hunter_threshold.py`
- Lines: 12

### `patch_importer_hunter.py`
- Lines: 17

### `patch_inventory.py`
- Lines: 13

### `patch_normalize_seo.py`
- Lines: 23

### `patch_promotion_rules.py`
- Lines: 22

### `patch_seo_report.py`
- Lines: 12

### `run_server.py`
- Lines: 22
- Functions: base_dir

### `scan_project.py`
- Lines: 126

### `scripts\smoke_test.py`
- Lines: 56
- Functions: assert_ok

### `tests\test_customer_support_ai.py`
- Lines: 66
- Functions: test_support_classifies_tracking_message, test_support_escalates_legal_threat, test_support_reply_auto_send_blocked_when_escalated, test_support_reply_includes_tracking_from_fulfillment_context, test_support_high_value_order_escalates

### `tests\test_fulfillment_agent.py`
- Lines: 91
- Functions: _address, _request, test_fulfillment_api_endpoint

### `tests\test_marketplace_module.py`
- Lines: 87
- Functions: test_listing_builder_uses_best_supplier_offer, test_marketplace_api_publish_and_orders

### `tests\test_product_hunter.py`
- Lines: 50
- Functions: test_demand_estimator_is_deterministic, test_hunter_api_endpoint

### `tests\test_self_learning_adaptation.py`
- Lines: 90
- Functions: event, test_learning_engine_recommends_scaling_profitable_sku, test_learning_engine_detects_bad_refund_rate, test_supplier_scores_penalize_complaints_and_late_delivery, test_adaptation_api_endpoint

### `tests\test_semi_auto_workflow.py`
- Lines: 33
- Functions: test_semi_auto_workflow_generates_results_safely, test_dashboard_can_enable_semi_auto_controls

### `tests\test_shipping_module.py`
- Lines: 75
- Functions: sample_rate_request, test_shipping_api_endpoints_work

## ??????? ????????

### `app\add_test_tracking.py`
- Lines: 20
- Logs: app/logs/tracking_updates.json

### `app\click_tracking_init.py`
- Lines: 51
- Logs: app/logs/click_tracking_state.json, app/logs/imported_skus.json

### `app\conversion_tracking_validation.py`
- Lines: 45
- Functions: read_json
- Logs: app/logs/conversion_tracking_validation.json, app/logs/event_learning_sync.json, app/logs/meta_token_validation.json, app/logs/system_status_dashboard.json

### `app\push_tracking_to_channels.py`
- Lines: 52
- Logs: app/logs/tracking_push_results.json, app/logs/tracking_updates.json

### `app\tracking_sync.py`
- Lines: 35
- Logs: app/logs/cj_purchase_attempts.json, app/logs/tracking_updates.json

## ????????? / ?????? ???????

### `app\autopilot_report.py`
- Lines: 67
- Logs: app/logs/autopilot_run.json, app/logs/exploration_v2.json, app/logs/product_performance.json, app/logs/published_posts.json

### `app\autopilot_runner.py`
- Lines: 231
- Functions: run_step, shopify_catalog_ok
- Logs: app/logs/autopilot_run.json
- Runs steps: action_executor, amazon_token_refresher, auto_launch_engine, auto_publish_or_fallback, auto_scaling_score, auto_spend_executor, autonomous_fulfillment_status, autonomous_trend_filter, build_priority_queue, campaign_approval_queue, campaign_hub, ceo_dashboard, cj_paid_order_fulfillment, cj_trend_bridge, crm_personalized_drafts, crm_readiness_summary, customer_fulfillment_support_status, daily_summary, draft_listing_activation_plan, draft_listing_activator

### `app\autopilot_schedule_readiness.py`
- Lines: 46
- Functions: read_json
- Logs: app/logs/alerts.json, app/logs/autopilot_schedule_readiness.json, app/logs/backup_report.json, app/logs/recovery_report.json, app/logs/system_status_dashboard.json

### `app\fix_autopilot_crm_duplicates.py`
- Lines: 28
- Runs steps: crm_personalized_drafts, shopify_crm_events

### `app\fix_autopilot_indent.py`
- Lines: 33
- Runs steps: crm_readiness_summary, etsy_autopilot, etsy_connection_status

### `app\main_AUTOPILOT_NO_DUPES_OK.py`
- Lines: 1853
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_AUTOPILOT_SAFE_FLOW_OK.py`
- Lines: 1853
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\patch_auto_scaling_runner.py`
- Lines: 17
- Runs steps: auto_scaling_score, daily_summary

### `app\patch_auto_spend_runner.py`
- Lines: 18
- Runs steps: auto_launch_engine, auto_spend_executor, ceo_dashboard

### `app\patch_autopilot_crm_drafts.py`
- Lines: 16
- Runs steps: crm_personalized_drafts, daily_summary, shopify_crm_events

### `app\patch_autopilot_exploration_v2.py`
- Lines: 16
- Runs steps: exploration_engine, exploration_engine_v2

### `app\patch_autopilot_priority_queue.py`
- Lines: 14
- Runs steps: build_priority_queue, exploration_engine_v2

### `app\patch_autopilot_publish_plan.py`
- Lines: 14
- Runs steps: build_priority_queue, publish_execution_plan

### `app\patch_autopilot_system_status.py`
- Lines: 14
- Runs steps: daily_summary, system_status_report

### `app\patch_ceo_dashboard_runner.py`
- Lines: 17
- Runs steps: ceo_dashboard, roi_simulation

### `app\patch_emergency_stop_runner.py`
- Lines: 17
- Runs steps: emergency_stop_validator, hourly_budget_monitor

### `app\patch_guardrails_runner.py`
- Lines: 17
- Runs steps: auto_scaling_score, product_guardrails

### `app\patch_hourly_budget_runner.py`
- Lines: 17
- Runs steps: hourly_budget_monitor, negative_roi_auto_pause

### `app\patch_live_api_gate_runner.py`
- Lines: 17
- Runs steps: live_api_execution_gate, live_campaign_registry

### `app\patch_live_audit_ledger_runner.py`
- Lines: 17
- Runs steps: live_execution_consolidator, live_spend_audit_ledger

### `app\patch_live_audit_reader_runner.py`
- Lines: 17
- Runs steps: live_spend_audit_ledger, live_spend_audit_reader

### `app\patch_live_backend_router_runner.py`
- Lines: 17
- Runs steps: live_backend_router, live_spend_permission_gate

### `app\patch_live_campaign_registry_runner.py`
- Lines: 17
- Runs steps: google_live_campaign_builder, live_campaign_registry

### `app\patch_live_consolidator_runner.py`
- Lines: 17
- Runs steps: google_live_executor, live_execution_consolidator

### `app\patch_live_execution_reporter_runner.py`
- Lines: 17
- Runs steps: live_api_execution_gate, live_execution_reporter

### `app\patch_live_executors_runner.py`
- Lines: 18
- Runs steps: google_live_executor, live_mode_final_lock, meta_live_executor

### `app\patch_live_gate_runner.py`
- Lines: 17
- Runs steps: emergency_stop_validator, live_spend_permission_gate

### `app\patch_live_mode_final_lock_runner.py`
- Lines: 17
- Runs steps: live_execution_reporter, live_mode_final_lock

### `app\patch_spend_history_runner.py`
- Lines: 17
- Runs steps: auto_spend_executor, spend_history_tracker

### `app\pipeline_runner.py`
- Lines: 64
- Logs: app/logs/pipeline_runner_results.json

### `app\product_hunter_runner.py`
- Lines: 29

### `patch_hunter_runner_registry.py`
- Lines: 12

## ????????? / CJ Dropshipping / ???????

### `app\check_cj_status.py`
- Lines: 7
- ENV: SUPPLIER_API_KEY

### `app\cj_customer_address_validator.py`
- Lines: 50
- Logs: app/logs/cj_customer_address_validator.json, app/logs/cj_order_payloads.json

### `app\cj_order_draft_creator.py`
- Lines: 57
- Logs: app/logs/cj_order_draft_creator.json, app/logs/cj_order_drafts.json, app/logs/supplier_purchase_queue.json

### `app\cj_payload_builder.py`
- Lines: 60
- Logs: app/logs/cj_order_drafts.json, app/logs/cj_order_payloads.json, app/logs/cj_payload_builder.json, app/logs/cj_product_mapping.json

### `app\cj_product_detail.py`
- Lines: 43
- ENV: CJ_ACCESS_TOKEN
- Logs: app/logs/cj_product_detail.json

### `app\cj_product_search.py`
- Lines: 49
- ENV: CJ_ACCESS_TOKEN, CJ_SEARCH_KEYWORD
- Logs: app/logs/cj_product_search.json

### `app\cj_purchase_executor.py`
- Lines: 67
- Logs: app/logs/cj_purchase_attempts.json, app/logs/supplier_purchase_queue.json

### `app\cj_supplier_readiness.py`
- Lines: 29
- ENV: CJ_ACCESS_TOKEN, CJ_PLATFORM_TOKEN
- Logs: app/logs/cj_supplier_readiness.json

### `app\import_supplier_products.py`
- Lines: 161
- ENV: DRY_RUN, IMPORT_EXISTING_ACTION, SUPPLIER_LIMIT, SUPPLIER_MODE

### `app\supplier_fallback_engine.py`
- Lines: 57
- Functions: read_json
- Logs: app/logs/cj_supplier_readiness.json, app/logs/supplier_fallback_engine.json

### `app\supplier_purchase_executor.py`
- Lines: 32
- Logs: app/logs/supplier_purchase_executor.json, app/logs/supplier_purchase_queue.json

### `app\supplier_purchase_queue.py`
- Lines: 43
- Logs: app/logs/imported_skus.json, app/logs/incoming_orders.json, app/logs/supplier_purchase_queue.json

### `app\suppliers\mock_real_supplier.py`
- Lines: 7

### `app\suppliers\mock_supplier.py`
- Lines: 107
- Classes: MockSupplierClient
- Functions: __init__, _default_catalog

### `app\suppliers\real_supplier.py`
- Lines: 79
- Functions: extract_products, save_env_value, refresh_cj_access_token, fetch_real_supplier_products
- ENV: CJ_API_TOKEN, CJ_API_URL, CJ_EMAIL, SUPPLIER_API_URL, SUPPLIER_PRODUCTS_ENDPOINT, SUPPLIER_PRODUCTS_PATH

### `app\suppliers\sandbox_supplier.py`
- Lines: 16
- Functions: fetch_supplier_products

### `app\suppliers\supplier_env_validator.py`
- Lines: 27
- ENV: SUPPLIER_API_KEY, SUPPLIER_API_URL

### `app\test_real_supplier.py`
- Lines: 17

### `app\test_supplier_connection.py`
- Lines: 52
- ENV: SUPPLIER_API_KEY, SUPPLIER_API_URL

### `app\upgrade\supplier_sandbox.py`
- Lines: 32
- Classes: SupplierSandboxClient
- Functions: __init__, search_products, create_purchase_order

### `patch_cj_refresh.py`
- Lines: 44
- ENV: CJ_API_TOKEN, CJ_API_URL, CJ_EMAIL, SUPPLIER_API_URL

### `patch_supplier.py`
- Lines: 17
- ENV: SUPPLIER_PRODUCTS_ENDPOINT, SUPPLIER_PRODUCTS_PATH

### `tests\test_supplier_module.py`
- Lines: 48
- Functions: test_currency_converter_round_trip_supported_currency, test_normalizer_creates_core_supplier_offer, test_supplier_search_api_endpoint

## ?????????? ?????????

### `app\auto_publish_or_fallback.py`
- Lines: 93
- ENV: META_PAGE_ACCESS_TOKEN, META_PAGE_ID
- Logs: app/logs/auto_publish_or_fallback_result.json, app/logs/published_posts.json

### `app\daily_publish_guard.py`
- Lines: 21
- Logs: app/logs/daily_publish_lock.json

### `app\engines\publish_registry.py`
- Lines: 131

### `app\generate_publish_queue.py`
- Lines: 54

### `app\listing_publish_execution_plan.py`
- Lines: 39
- Functions: read_json
- Logs: app/logs/listing_publish_execution_plan.json, app/logs/listing_publish_validator.json

### `app\listing_publish_validator.py`
- Lines: 51
- Functions: read_json
- Logs: app/logs/global_channel_status_summary.json, app/logs/listing_publish_validator.json, app/logs/listing_publisher_plan.json

### `app\listing_publisher_plan.py`
- Lines: 42
- Functions: read_json
- Logs: app/logs/listing_publisher_plan.json, app/logs/organic_money_launch_plan.json

### `app\marketplaces\listing_builder.py`
- Lines: 32
- Classes: MarketplaceListingBuilder
- Functions: _slug, build_from_candidate

### `app\one_click_publish_helper.py`
- Lines: 18

### `app\publish_dog_socks_with_image.py`
- Lines: 49
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_SHOP, SHOPIFY_SHOP_DOMAIN

### `app\publish_execution_plan.py`
- Lines: 36
- Logs: app/logs/autopilot_priority_queue.json, app/logs/publish_execution_plan.json

### `app\services\listing_agent.py`
- Lines: 27
- Classes: ListingAgent
- Functions: generate_listing

### `app\smart_generate_publish_queue.py`
- Lines: 83
- Logs: app/logs/autopilot_decisions.json, app/logs/exploration_candidates.json, app/logs/product_catalog.json, app/logs/product_performance.json

### `app\social_auto_publish.py`
- Lines: 74
- ENV: META_PAGE_ACCESS_TOKEN, META_PAGE_ID
- Logs: app/logs/daily_social_posts_ready.json, app/logs/social_auto_publish_results.json

### `app\suppliers\listing_optimizer.py`
- Lines: 15

### `patch_publish_hunter_sku.py`
- Lines: 19

### `tests\test_auto_listing_generator.py`
- Lines: 44
- Functions: test_listing_generator_creates_marketplace_safe_listing, test_listing_generator_blocks_dangerous_terms, test_listing_generator_strips_html_and_has_defaults

## ?????????? Etsy

### `app\channels\etsy_adapter.py`
- Lines: 22

### `app\etsy_auth_url.py`
- Lines: 35
- ENV: ETSY_API_KEY, ETSY_CLIENT_ID, ETSY_REDIRECT_URI

### `app\etsy_autopilot.py`
- Lines: 27
- ENV: ETSY_ACCESS_TOKEN
- Logs: app/logs/etsy_autopilot.json

### `app\etsy_connection_status.py`
- Lines: 51
- Logs: app/logs/etsy_connection_status.json

### `app\etsy_oauth_exchange.py`
- Lines: 72
- ENV: ETSY_API_KEY, ETSY_AUTH_CODE, ETSY_CLIENT_ID, ETSY_REDIRECT_URI
- Logs: app/logs/etsy_oauth_exchange.json

### `app\patch_autopilot_etsy.py`
- Lines: 16
- Runs steps: crm_readiness_summary, etsy_autopilot, etsy_connection_status

### `app\patch_status_etsy.py`
- Lines: 22
- Logs: app/logs/etsy_autopilot.json, app/logs/etsy_connection_status.json

## ?????????? Shopify

### `app\channels\shopify_adapter.py`
- Lines: 287
- ENV: SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\channels\shopify_config.py`
- Lines: 27
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_DOMAIN, SHOPIFY_STORE_URL

### `app\debug_shopify_crm_source.py`
- Lines: 30
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL

### `app\debug_shopify_env.py`
- Lines: 12
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_SHOP, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL

### `app\delete_shopify_duplicate.py`
- Lines: 18
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_SHOP, SHOPIFY_SHOP_DOMAIN

### `app\feeds\meta_shopify_feed.py`
- Lines: 89
- Logs: app/logs/imported_skus.json

### `app\final_mvp\shopify.py`
- Lines: 56
- Classes: ShopifyDraftService
- Functions: __init__, configured, headers
- ENV: DRY_RUN, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL

### `app\import_shopify_products.py`
- Lines: 53
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL
- Logs: app/logs/product_catalog.json

### `app\import_shopify_results.py`
- Lines: 85
- Logs: app/logs/imported_sales_files.json, app/logs/product_performance.json

### `app\main_STABLE_AI_SHOPIFY_PIPELINE.py`
- Lines: 1888
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_WITH_SHOPIFY_AUTO_MODULE_OK.py`
- Lines: 1892
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_WORKING_SHOPIFY_OK.py`
- Lines: 1719
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\main_before_shopify_fallback.py`
- Lines: 2683
- ENV: ADS_ENABLED, AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, AUTO_PUBLISH_ENABLED, CJ_ACCESS_TOKEN, DRY_RUN, EMERGENCY_STOP, GOOGLE_ADS_ENABLED, MAX_DAILY_AD_SPEND, META_ACCESS_TOKEN, META_ADS_ENABLED, META_AD_ACCOUNT_ID, META_PIXEL_ID, MIN_MARGIN_PERCENT
- Logs: app/logs/imported_skus.json

### `app\marketplaces\shopify_marketplace.py`
- Lines: 139
- Classes: ShopifyMarketplaceClient
- Functions: __init__, name, configured

### `app\patch_autopilot_shopify_refresh.py`
- Lines: 13
- Runs steps: daily_publish_guard, refresh_shopify_token

### `app\refresh_shopify_token.py`
- Lines: 121
- Logs: app/logs/shopify_token_refresh.json

### `app\services\shopify_client.py`
- Lines: 23
- Classes: ShopifyClient
- Functions: __init__

### `app\shopify_autopilot.py`
- Lines: 82
- Functions: validate, refresh
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET, SHOPIFY_STORE_URL

### `app\shopify_catalog_issues.py`
- Lines: 42
- Logs: app/logs/shopify_catalog_issues.json, app/logs/shopify_product_report.json

### `app\shopify_cleanup_titles.py`
- Lines: 39
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL

### `app\shopify_crm_events.py`
- Lines: 83
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL
- Logs: app/logs/shopify_crm_events.json

### `app\shopify_delete_bad_products.py`
- Lines: 34
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP, SHOPIFY_SHOP_DOMAIN, SHOPIFY_STORE_URL

### `app\shopify_product_report.py`
- Lines: 68
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_SHOP, SHOPIFY_STORE, SHOPIFY_STORE_URL, SHOPIFY_TOKEN
- Logs: app/logs/shopify_product_report.json

### `app\shopify_registry_hydrator.py`
- Lines: 160
- Functions: load_env_file, normalize_shop_domain
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_SHOP, SHOPIFY_STORE_DOMAIN, SHOPIFY_STORE_URL
- Logs: app/logs/imported_skus.json, app/logs/shopify_registry_hydration_results.json

### `app\shopify_token_auto_repair.py`
- Lines: 151
- Functions: update_env, check_token, repair
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET, SHOPIFY_SHOP_DOMAIN
- Logs: app/logs/shopify_token_auto_repair.json

### `app\shopify_write_validation.py`
- Lines: 78
- Functions: load_env, shop_domain
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL
- Logs: app/logs/imported_skus.json, app/logs/shopify_write_validation.json

### `app\suppliers\shopify_mapper.py`
- Lines: 29

### `app\sync_hunter_to_shopify.py`
- Lines: 77
- Logs: app/logs/imported_skus.json

### `app\sync_shopify_orders.py`
- Lines: 43
- Logs: app/logs/imported_skus.json

### `app\update_shopify_existing.py`
- Lines: 85
- Logs: app/logs/imported_skus.json

### `app\upgrade\shopify_client.py`
- Lines: 55
- Classes: ShopifyClient
- Functions: __init__, from_env, is_configured, status
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL

### `check_shopify_env.py`
- Lines: 16

### `fix_shopify_env.py`
- Lines: 15

### `patch_meta_shopify_retry.py`
- Lines: 31

### `patch_shopify_token.py`
- Lines: 15
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN

### `patch_shopify_url.py`
- Lines: 18

### `patch_update_shopify_config.py`
- Lines: 25

### `shopify_full_check.py`
- Lines: 71

## ?????????? WooCommerce

### `app\channels\woocommerce_adapter.py`
- Lines: 22

### `app\channels\woocommerce_gateway.py`
- Lines: 300
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\fix_woocommerce_validation_url.py`
- Lines: 12
- ENV: WOOCOMMERCE_STORE_URL, WOOCOMMERCE_URL

### `app\woocommerce_category_fix.py`
- Lines: 91
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_category_fix_result.json

### `app\woocommerce_draft_enricher.py`
- Lines: 93
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_draft_enrichment_result.json

### `app\woocommerce_draft_publisher.py`
- Lines: 87
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_draft_publish_result.json

### `app\woocommerce_final_publisher.py`
- Lines: 60
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_publish_result.json

### `app\woocommerce_image_auto_upload.py`
- Lines: 100
- Functions: wp_headers, upload_media, update_product_image
- Logs: app/logs/woocommerce_image_auto_upload_report.json

### `app\woocommerce_image_gap_report.py`
- Lines: 48
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_image_gap_report.json

### `app\woocommerce_image_manual_action.py`
- Lines: 28
- Logs: app/logs/woocommerce_image_manual_action.json

### `app\woocommerce_listing_publisher.py`
- Lines: 33
- Functions: read_json
- Logs: app/logs/listing_publish_execution_plan.json, app/logs/woocommerce_listing_publisher.json

### `app\woocommerce_live_publish_guard.py`
- Lines: 29
- Functions: read_json
- Logs: app/logs/woocommerce_listing_publisher.json, app/logs/woocommerce_live_publish_guard.json

### `app\woocommerce_local_image_upload.py`
- Lines: 111
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_local_image_upload.json

### `app\woocommerce_order_monitor.py`
- Lines: 52
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_order_monitor.json

### `app\woocommerce_placeholder_images.py`
- Lines: 62
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_placeholder_images.json

### `app\woocommerce_pre_publish_check.py`
- Lines: 66
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/woocommerce_pre_publish_check.json

### `app\woocommerce_real_publisher.py`
- Lines: 39
- Functions: read_json
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_URL
- Logs: app/logs/listing_publish_execution_plan.json, app/logs/woocommerce_real_publisher.json

### `app\woocommerce_validation.py`
- Lines: 73
- Functions: load_env
- ENV: WC_CONSUMER_KEY, WC_CONSUMER_SECRET, WC_STORE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL, WOOCOMMERCE_URL, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, WOO_STORE_URL
- Logs: app/logs/woocommerce_validation.json

### `app\woocommerce_write_validation.py`
- Lines: 89
- Functions: load_env
- ENV: WC_CONSUMER_KEY, WC_CONSUMER_SECRET, WC_STORE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL, WOO_CONSUMER_KEY, WOO_CONSUMER_SECRET, WOO_STORE_URL
- Logs: app/logs/woocommerce_write_validation.json

## ?????????? eBay

### `app\channels\ebay_adapter.py`
- Lines: 22

### `app\channels\ebay_gateway.py`
- Lines: 311
- Functions: ebay_config, ebay_get_access_token, ebay_headers, ebay_live_check, ebay_get_inventory_item, ebay_create_inventory_item, ebay_create_offer, ebay_create_location, ebay_publish_offer
- ENV: DEFAULT_CURRENCY, EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_MARKETPLACE_ID, EBAY_REFRESH_TOKEN, EBAY_TOKEN_URL

### `app\channels\ebay_gateway_ACCESS_TOKEN_OK.py`
- Lines: 149
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_MARKETPLACE_ID, EBAY_REFRESH_TOKEN, EBAY_TOKEN_URL

### `app\channels\ebay_gateway_CONNECTED_OK.py`
- Lines: 149
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_MARKETPLACE_ID, EBAY_REFRESH_TOKEN, EBAY_TOKEN_URL

### `app\channels\ebay_gateway_INVENTORY_ITEM_OK.py`
- Lines: 193
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_MARKETPLACE_ID, EBAY_REFRESH_TOKEN, EBAY_TOKEN_URL

### `app\check_ebay_env_safe.py`
- Lines: 17

### `app\commerce\routes_EBAY_CONNECTED_OK.py`
- Lines: 145
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\commerce\routes_EBAY_OVERVIEW_CONNECTED_OK.py`
- Lines: 146
- ENV: WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET, WOOCOMMERCE_STORE_URL

### `app\ebay_read_validation.py`
- Lines: 75
- Functions: load_env
- ENV: EBAY_ACCESS_TOKEN, EBAY_OAUTH_TOKEN, EBAY_USER_TOKEN
- Logs: app/logs/ebay_read_validation.json, app/logs/imported_skus.json

### `app\ebay_write_offer_validation.py`
- Lines: 116
- Functions: load_env
- ENV: EBAY_ACCESS_TOKEN, EBAY_API_BASE, EBAY_OAUTH_TOKEN, EBAY_USER_TOKEN
- Logs: app/logs/ebay_write_offer_validation.json, app/logs/imported_skus.json

### `app\ebay_write_validation.py`
- Lines: 97
- Functions: load_env
- ENV: EBAY_ACCESS_TOKEN, EBAY_OAUTH_TOKEN, EBAY_USER_TOKEN
- Logs: app/logs/ebay_write_validation.json, app/logs/imported_skus.json

### `app\publish_ebay_from_imports.py`
- Lines: 131
- Logs: app/logs/ebay_published_skus.json, app/logs/imported_skus.json

### `app\publish_ebay_test.py`
- Lines: 25

### `app\refresh_ebay_token.py`
- Lines: 51
- Functions: refresh_ebay_access_token
- ENV: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN

### `app\sync_ebay_orders.py`
- Lines: 15
- Logs: app/logs/imported_skus.json

### `backfill_ebay_metadata.py`
- Lines: 24
- Logs: app/logs/ebay_published_skus.json, app/logs/imported_skus.json

### `create_ebay_location.py`
- Lines: 42
- ENV: EBAY_ACCESS_TOKEN

### `get_ebay_tokens.py`
- Lines: 69
- Functions: replace_or_add
- ENV: EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REDIRECT_URI

### `patch_ebay_inventory.py`
- Lines: 54

### `patch_ebay_inventory_headers.py`
- Lines: 27

### `patch_ebay_logging.py`
- Lines: 33

### `patch_ebay_metadata.py`
- Lines: 31

### `patch_ebay_policy_auto.py`
- Lines: 44

### `patch_ebay_real_data.py`
- Lines: 32

### `patch_ebay_real_data_fix.py`
- Lines: 29

### `patch_ebay_sync_delay.py`
- Lines: 20

### `patch_ebay_title_length.py`
- Lines: 12

### `patch_pipeline_summary_ebay.py`
- Lines: 12

### `test_real_ebay.py`
- Lines: 25

## ???????????? / ???????????

### `app\arbitrage_safety_gate.py`
- Lines: 79
- Logs: app/logs/arbitrage_decisions.json, app/logs/arbitrage_safety_gate.json, app/logs/imported_skus.json

### `app\crm_send_guard.py`
- Lines: 29
- Functions: read_json
- Logs: app/logs/OWNER_CONFIRM_CRM_SEND.json, app/logs/crm_message_generator.json, app/logs/crm_send_guard.json

### `app\engines\guard.py`
- Lines: 64

### `app\engines\risk_guard.py`
- Lines: 51

### `app\fulfillment_guard.py`
- Lines: 40
- Functions: check_fulfillment_allowed

### `app\inventory_sync_guard.py`
- Lines: 44
- Functions: read_json
- Logs: app/logs/global_arbitrage_engine.json, app/logs/inventory_sync_guard.json, app/logs/registry_quality_report.json, app/logs/supplier_fallback_engine.json

### `app\niche_exclusion_guard.py`
- Lines: 52
- Functions: read_json
- Logs: app/logs/ai_pricing_engine.json, app/logs/niche_exclusion_guard.json, app/logs/niche_exclusion_registry.json, app/logs/real_traffic_launcher.json

### `app\patch_pre_guard_planning.py`
- Lines: 19
- Runs steps: build_priority_queue, crm_readiness_summary, exploration_engine_v2, publish_execution_plan

### `app\product_guardrails.py`
- Lines: 55
- Logs: app/logs/product_guardrails.json

### `app\production\safety.py`
- Lines: 44
- Functions: safety_check

### `app\runtime_safety.py`
- Lines: 14
- ENV: DRY_RUN, SUPPLIER_MODE

### `app\suppliers\product_safety.py`
- Lines: 44

### `app\test_fulfillment_guard.py`
- Lines: 19

## Dashboard / UI backend

### `app\ceo_dashboard.py`
- Lines: 72
- Functions: load

### `app\dashboard\__init__.py`
- Lines: 1

### `app\dashboard\schemas.py`
- Lines: 27
- Classes: AutonomyControls, DashboardStatus, DashboardMetrics

### `app\dashboard\service.py`
- Lines: 66
- Classes: DashboardService
- Functions: __init__, get_status, update_controls, get_metrics

### `app\dashboard_report.py`
- Lines: 53

### `app\main_DASHBOARD_WORKING_OK.py`
- Lines: 1892
- Functions: load_env_local, health, evaluate_product, list_marketplaces, advanced_evaluate, profit_scenarios, generate_listing, list_shipping_carriers, classify_support_message, draft_support_reply, analyze_adaptation, admin_dashboard, dashboard_status, dashboard_metrics, dashboard_controls
- ENV: AUTONOMY_ENABLED, AUTOPILOT_INTERVAL_HOURS, AUTOPILOT_KEYWORDS, AUTOPILOT_MAX_REAL_DRAFTS, AUTOPILOT_MIN_SCORE, AUTOPILOT_SCHEDULE_ENABLED, AUTOPUBLISH_ENABLED, AUTOPUBLISH_MIN_MARGIN, DRY_RUN, EMERGENCY_STOP, MIN_MARGIN_PERCENT, MIN_SELL_PRICE, OPENAI_API_KEY, OPENAI_MODEL, PRICE_MULTIPLIER, SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_API_VERSION, SHOPIFY_STORE_URL, SUPPLIER_API_KEY
- Logs: app/logs/imported_skus.json

### `app\shopify_automation\routes_DASHBOARD_CARDS_OK.py`
- Lines: 559
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog, orders_sync, orders_summary, shopify_automation_dashboard
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\shopify_automation\routes_DASHBOARD_STATUS_OK.py`
- Lines: 559
- Functions: shopify_auto_health, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_product, auto_publish_evaluate_catalog, auto_publish_evaluate_catalog_safe, auto_publish_run, pricing_optimize, pricing_preview_catalog, pricing_optimize, pricing_preview_catalog, pricing_apply_catalog, orders_sync, orders_summary, shopify_automation_dashboard
- ENV: SHOPIFY_ACCESS_TOKEN, SHOPIFY_ADMIN_TOKEN, SHOPIFY_STORE_URL

### `app\system_health_dashboard.py`
- Lines: 58
- Logs: app/logs/imported_skus.json, app/logs/seo_push_summary.json, app/logs/seo_quality_report.json, app/logs/seo_repush_execution.json, app/logs/system_health_dashboard.json

### `app\system_status_dashboard.py`
- Lines: 39
- Functions: read_json
- Logs: app/logs/channel_self_healer.json, app/logs/external_blockers_monitor.json, app/logs/global_commerce_control_panel.json, app/logs/production_readiness_report.json, app/logs/system_status_dashboard.json

### `tests\test_admin_dashboard.py`
- Lines: 39
- Functions: test_dashboard_status_exposes_all_modules, test_dashboard_metrics_is_safe_default, test_emergency_stop_forces_autonomy_off, test_dashboard_html_loads

## Google Ads / Google Feed

### `app\channels\google_merchant_adapter.py`
- Lines: 17

### `app\feeds\google_merchant_feed.py`
- Lines: 89
- Logs: app/logs/imported_skus.json

### `app\google_access_monitor.py`
- Lines: 52
- Logs: app/logs/google_access_monitor.json

### `app\google_access_status.py`
- Lines: 28
- ENV: GOOGLE_ADS_CUSTOMER_ID, GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_REFRESH_TOKEN
- Logs: app/logs/google_access_status.json

### `app\google_activation_readiness_gate.py`
- Lines: 55
- Functions: read_json
- Logs: app/logs/budget_controller.json, app/logs/compliance_layer.json, app/logs/external_blockers_monitor.json, app/logs/google_activation_readiness_gate.json, app/logs/google_campaign_live_creator.json, app/logs/product_quality_filter.json, app/logs/system_status_dashboard.json

### `app\google_ad_drafts_from_content.py`
- Lines: 39
- Logs: app/logs/google_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app\google_ads_readiness.py`
- Lines: 44
- Functions: load_env
- ENV: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_CUSTOMER_ID, GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_REFRESH_TOKEN
- Logs: app/logs/google_ads_readiness.json

### `app\google_ads_token_refresher.py`
- Lines: 82
- Functions: update_env
- ENV: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN
- Logs: app/logs/google_ads_token_refresher.json

### `app\google_campaign_live_creator.py`
- Lines: 69
- Logs: app/logs/ad_campaign_executor.json, app/logs/google_api_guard.json, app/logs/google_campaign_live_creator.json

### `app\google_campaign_live_poster.py`
- Lines: 92
- ENV: GOOGLE_ADS_CUSTOMER_ID
- Logs: app/logs/google_api_guard.json, app/logs/google_campaign_live_creator.json, app/logs/google_campaign_live_result.json

### `app\google_live_campaign_builder.py`
- Lines: 38
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/live_backend_router.json

### `app\google_live_executor.py`
- Lines: 66
- Logs: app/logs/google_live_campaign_payloads.json, app/logs/google_live_execution_result.json, app/logs/live_mode_final_lock.json

### `app\google_payload_safe_creator.py`
- Lines: 38
- Logs: app/logs/campaign_executor.json, app/logs/google_campaign_live_creator.json

### `app\google_refresh_token.py`
- Lines: 61

### `app\patch_google_ad_drafts.py`
- Lines: 15
- Runs steps: google_ad_drafts_from_content, meta_ad_drafts_from_content

### `app\patch_google_live_builder_runner.py`
- Lines: 17
- Runs steps: google_live_campaign_builder, meta_live_campaign_builder

### `create_google_merchant_feed.py`
- Lines: 20

## Meta / Facebook / Instagram

### `app\channels\meta_adapter.py`
- Lines: 54
- ENV: META_ACCESS_TOKEN, META_CATALOG_ID

### `app\channels\meta_channel.py`
- Lines: 24

### `app\channels\meta_shop_adapter.py`
- Lines: 17

### `app\check_meta_ads.py`
- Lines: 28
- ENV: META_ACCESS_TOKEN, META_API_VERSION

### `app\check_meta_adsets.py`
- Lines: 29
- ENV: META_ACCESS_TOKEN, META_API_VERSION

### `app\feeds\meta_feed.py`
- Lines: 109

### `app\fix_meta_account_id.py`
- Lines: 22

### `app\fix_meta_budget_sharing.py`
- Lines: 20

### `app\fix_meta_objective.py`
- Lines: 14

### `app\fix_meta_special_categories.py`
- Lines: 13

### `app\meta_activate_ad.py`
- Lines: 38
- ENV: META_ACCESS_TOKEN, META_API_VERSION
- Logs: app/logs/meta_ad_builder_result.json

### `app\meta_activate_adset.py`
- Lines: 36
- ENV: META_ACCESS_TOKEN, META_API_VERSION
- Logs: app/logs/meta_ad_builder_result.json

### `app\meta_activate_campaign.py`
- Lines: 36
- ENV: META_ACCESS_TOKEN, META_API_VERSION
- Logs: app/logs/meta_live_execution_result.json

### `app\meta_activation_executor.py`
- Lines: 44
- Logs: app/logs/meta_activation_executor.json, app/logs/meta_activation_guard.json, app/logs/meta_safe_activation_plan.json

### `app\meta_activation_readiness_gate.py`
- Lines: 50
- Functions: read_json
- Logs: app/logs/OWNER_CONFIRM_META_ACTIVATION.json, app/logs/budget_controller.json, app/logs/compliance_layer.json, app/logs/meta_activation_readiness_gate.json, app/logs/meta_safe_activation_plan.json, app/logs/product_quality_filter.json, app/logs/system_status_dashboard.json

### `app\meta_ad_accounts.py`
- Lines: 53
- Functions: load_env
- ENV: META_ACCESS_TOKEN
- Logs: app/logs/meta_ad_accounts.json

### `app\meta_ad_builder.py`
- Lines: 76
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION
- Logs: app/logs/meta_ad_builder_result.json, app/logs/meta_adset_builder_result.json, app/logs/meta_creative_builder_result.json

### `app\meta_ad_drafts_from_content.py`
- Lines: 32
- Logs: app/logs/meta_ad_drafts_from_content.json, app/logs/social_content_enhanced.json

### `app\meta_ads_live_creator.py`
- Lines: 35
- Logs: app/logs/meta_ads_live_creator.json, app/logs/meta_creative_live_creator.json

### `app\meta_ads_readiness.py`
- Lines: 42
- Functions: load_env
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_PIXEL_ID
- Logs: app/logs/meta_ads_readiness.json

### `app\meta_adset_builder.py`
- Lines: 79
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION, META_PIXEL_ID
- Logs: app/logs/meta_adset_builder_result.json, app/logs/meta_live_execution_result.json

### `app\meta_adset_live_creator.py`
- Lines: 37
- Logs: app/logs/meta_adset_live_creator.json, app/logs/meta_campaign_registry.json

### `app\meta_assets_discovery.py`
- Lines: 40
- Functions: load_env, call
- ENV: META_ACCESS_TOKEN
- Logs: app/logs/meta_assets_discovery.json

### `app\meta_auto_stop_monitor.py`
- Lines: 40
- Logs: app/logs/meta_activation_executor.json, app/logs/meta_auto_stop_monitor.json, app/logs/real_sales_mode.json

### `app\meta_business_assets.py`
- Lines: 48
- Functions: load_env, call
- ENV: META_ACCESS_TOKEN, META_BUSINESS_ID
- Logs: app/logs/meta_business_assets.json

### `app\meta_business_sync.py`
- Lines: 30
- Logs: app/logs/meta_assets_discovery.json

### `app\meta_campaign_live_creator.py`
- Lines: 69
- Logs: app/logs/ad_campaign_executor.json, app/logs/meta_api_guard.json, app/logs/meta_campaign_live_creator.json

### `app\meta_campaign_live_poster.py`
- Lines: 63
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_GRAPH_API_VERSION
- Logs: app/logs/meta_api_guard.json, app/logs/meta_campaign_live_creator.json, app/logs/meta_campaign_live_result.json

### `app\meta_campaign_registry_sync.py`
- Lines: 32
- Logs: app/logs/meta_campaign_live_result.json, app/logs/meta_campaign_registry.json

### `app\meta_connection_status.py`
- Lines: 43
- Functions: count_items
- Logs: app/logs/meta_business_assets.json, app/logs/meta_connection_status.json

### `app\meta_creative_builder.py`
- Lines: 87
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION, META_PAGE_ID, SHOPIFY_PRODUCT_URL
- Logs: app/logs/meta_adset_builder_result.json, app/logs/meta_creative_builder_result.json

### `app\meta_creative_live_creator.py`
- Lines: 45
- Logs: app/logs/meta_adset_live_creator.json, app/logs/meta_creative_live_creator.json, app/logs/opportunities/global_execution_plan.json

### `app\meta_debug_token.py`
- Lines: 21
- ENV: META_ACCESS_TOKEN, META_APP_ID, META_APP_SECRET, META_PAGE_ACCESS_TOKEN

### `app\meta_health.py`
- Lines: 37
- ENV: META_ACCESS_TOKEN, META_BUSINESS_ID, META_CATALOG_ID

### `app\meta_launch_readiness.py`
- Lines: 44
- Functions: load
- Logs: app/logs/meta_ads_live_creator.json, app/logs/meta_adset_live_creator.json, app/logs/meta_campaign_registry.json, app/logs/meta_creative_live_creator.json, app/logs/meta_launch_readiness.json

### `app\meta_live_campaign_builder.py`
- Lines: 38
- Logs: app/logs/live_backend_router.json, app/logs/meta_live_campaign_payloads.json

### `app\meta_live_executor.py`
- Lines: 90
- ENV: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION
- Logs: app/logs/live_mode_final_lock.json, app/logs/meta_live_campaign_payloads.json, app/logs/meta_live_execution_result.json

### `app\meta_page_post.py`
- Lines: 37
- ENV: META_ACCESS_TOKEN, META_PAGE_ACCESS_TOKEN, META_PAGE_ID
- Logs: app/logs/meta_page_post_result.json

### `app\meta_page_token_permissions.py`
- Lines: 16
- ENV: META_PAGE_ACCESS_TOKEN

### `app\meta_page_token_refresh.py`
- Lines: 66
- ENV: META_ACCESS_TOKEN, META_PAGE_ID
- Logs: app/logs/meta_page_token_refresh.json

### `app\meta_permission_url.py`
- Lines: 22

### `app\meta_safe_activation_plan.py`
- Lines: 48
- Logs: app/logs/global_commerce_control_panel.json, app/logs/meta_campaign_registry.json, app/logs/meta_safe_activation_plan.json

### `app\meta_test_event.py`
- Lines: 85
- Functions: sha256
- ENV: META_ACCESS_TOKEN, META_PIXEL_ID, META_TEST_EVENT_CODE
- Logs: app/logs/meta_test_event.json

### `app\meta_token_auto_repair.py`
- Lines: 119
- Functions: read_env, get_env_value, update_env, check
- Logs: app/logs/meta_token_auto_repair.json

### `app\meta_token_refresh.py`
- Lines: 126
- Functions: env_text, env_get, env_set
- Logs: app/logs/meta_token_refresh.json

### `app\meta_token_validation.py`
- Lines: 56
- Functions: load_env
- ENV: META_ACCESS_TOKEN
- Logs: app/logs/meta_token_validation.json

### `app\patch_meta_ad_drafts.py`
- Lines: 15
- Runs steps: meta_ad_drafts_from_content, social_content_enhancer

### `app\patch_meta_executor_env.py`
- Lines: 24
- ENV: META_ACCESS_TOKEN

### `app\patch_meta_live_builder_runner.py`
- Lines: 17
- Runs steps: live_backend_router, meta_live_campaign_builder

### `app\sync_meta_campaign_registry.py`
- Lines: 34
- Logs: app/logs/campaign_executor.json, app/logs/meta_campaign_registry.json

### `patch_meta_feed_loader.py`
- Lines: 27

### `patch_meta_feed_main.py`
- Lines: 26

### `patch_meta_feed_sources.py`
- Lines: 22

### `patch_meta_mapping.py`
- Lines: 75

### `patch_pipeline_meta.py`
- Lines: 13

### `test_meta.py`
- Lines: 10

## Product feed / ????

### `app\feed_channel_validation.py`
- Lines: 88
- Functions: load_json
- Logs: app/logs/feed_channel_validation.json, app/logs/google_feed_seo.json, app/logs/imported_skus.json, app/logs/meta_feed_seo.json

### `app\feed_mass_regenerator.py`
- Lines: 59
- Logs: app/logs/google_feed_seo.json, app/logs/imported_skus.json, app/logs/meta_feed_seo.json

### `app\feed_quality_check.py`
- Lines: 19
- Logs: app/logs/google_feed_seo.json, app/logs/meta_feed_seo.json

### `app\feed_regenerator.py`
- Lines: 70
- Logs: app/logs/feed_regeneration_results.json, app/logs/google_feed_seo.json, app/logs/imported_skus.json, app/logs/meta_feed_seo.json, app/logs/seo_push_results.json

### `app\hunter_feedback_engine.py`
- Lines: 75
- Logs: app/logs/hunter_feedback.json, app/logs/sales_roi_report.json
