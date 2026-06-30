# AICommerce Business Architecture Book

Created at: 2026-06-29T20:45:22.406168+00:00

## Purpose

This document maps business capabilities to existing modules, active autopilot steps, logs, and missing components.

## 1. Product Discovery

### Active autopilot steps
- **exploration_engine_v2** ? OK ? `app/exploration_engine_v2.py`
- **build_priority_queue** ? OK ? `app/build_priority_queue.py`
- **publish_execution_plan** ? OK ? `app/publish_execution_plan.py`
- **listing_publish_execution_plan_real** ? MISSING ? `app/listing_publish_execution_plan_real.py`

### Related project files
- `app/build_priority_queue.py` ? called_by_detected=yes, lines=30
- `app/engines/global_commerce_brain.py` ? called_by_detected=no, lines=439
- `app/exploration_engine_v2.py` ? called_by_detected=yes, lines=94
- `app/listing_publish_execution_plan.py` ? called_by_detected=no, lines=39
- `app/market_arbitrage_engine.py` ? called_by_detected=no, lines=89
- `app/multi_market_scanner.py` ? called_by_detected=no, lines=65
- `app/opportunity_engine.py` ? called_by_detected=no, lines=51
- `app/product_hunter/__init__.py` ? called_by_detected=no, lines=0
- `app/product_hunter/demand.py` ? called_by_detected=yes, lines=61
- `app/product_hunter/mapper.py` ? called_by_detected=yes, lines=61
- `app/product_hunter/schemas.py` ? called_by_detected=yes, lines=56
- `app/product_hunter/scoring.py` ? called_by_detected=yes, lines=38
- `app/product_hunter/service.py` ? called_by_detected=yes, lines=140
- `app/product_hunter_runner.py` ? called_by_detected=no, lines=29
- `app/publish_execution_plan.py` ? called_by_detected=yes, lines=36
- `tests/test_product_hunter.py` ? called_by_detected=no, lines=50

### Architecture note
This block finds candidates, scores them, and prepares a prioritized publish plan.

## 2. Supplier Intelligence

### Active autopilot steps
- **cj_paid_order_fulfillment** ? MISSING ? `app/cj_paid_order_fulfillment.py`
- **cj_trend_bridge** ? MISSING ? `app/cj_trend_bridge.py`
- **supplier_candidate_filter** ? MISSING ? `app/filter_supplier_candidates.py`

### Related project files
- `app/check_cj_status.py` ? called_by_detected=no, lines=7
- `app/cj_customer_address_validator.py` ? called_by_detected=no, lines=50
- `app/cj_order_draft_creator.py` ? called_by_detected=no, lines=57
- `app/cj_payload_builder.py` ? called_by_detected=no, lines=60
- `app/cj_product_detail.py` ? called_by_detected=no, lines=43
- `app/cj_product_search.py` ? called_by_detected=no, lines=49
- `app/cj_purchase_executor.py` ? called_by_detected=no, lines=67
- `app/cj_supplier_readiness.py` ? called_by_detected=no, lines=29
- `app/import_supplier_products.py` ? called_by_detected=no, lines=161
- `app/supplier_fallback_engine.py` ? called_by_detected=no, lines=57
- `app/supplier_purchase_executor.py` ? called_by_detected=no, lines=32
- `app/supplier_purchase_queue.py` ? called_by_detected=no, lines=43
- `app/suppliers/__init__.py` ? called_by_detected=no, lines=4
- `app/suppliers/ai_product_score.py` ? called_by_detected=yes, lines=58
- `app/suppliers/audit_log.py` ? called_by_detected=no, lines=19
- `app/suppliers/base.py` ? called_by_detected=yes, lines=31
- `app/suppliers/blocked_log.py` ? called_by_detected=no, lines=31
- `app/suppliers/currency.py` ? called_by_detected=yes, lines=30
- `app/suppliers/import_state.py` ? called_by_detected=no, lines=30
- `app/suppliers/listing_optimizer.py` ? called_by_detected=yes, lines=15
- `app/suppliers/mock_real_supplier.py` ? called_by_detected=no, lines=7
- `app/suppliers/mock_supplier.py` ? called_by_detected=yes, lines=107
- `app/suppliers/normalize_product.py` ? called_by_detected=yes, lines=56
- `app/suppliers/normalizer.py` ? called_by_detected=yes, lines=53
- `app/suppliers/pricing.py` ? called_by_detected=yes, lines=12
- `app/suppliers/product_safety.py` ? called_by_detected=no, lines=44
- `app/suppliers/real_supplier.py` ? called_by_detected=yes, lines=79
- `app/suppliers/registry.py` ? called_by_detected=yes, lines=31
- `app/suppliers/sandbox_supplier.py` ? called_by_detected=no, lines=16
- `app/suppliers/schemas.py` ? called_by_detected=yes, lines=70
- `app/suppliers/seo_mapper.py` ? called_by_detected=no, lines=33
- `app/suppliers/shopify_mapper.py` ? called_by_detected=no, lines=29
- `app/suppliers/stock_state.py` ? called_by_detected=no, lines=46
- `app/suppliers/supplier_env_validator.py` ? called_by_detected=no, lines=27
- `app/suppliers/title_optimizer.py` ? called_by_detected=no, lines=22
- `app/test_real_supplier.py` ? called_by_detected=no, lines=17
- `app/test_supplier_connection.py` ? called_by_detected=no, lines=52
- `app/upgrade/supplier_sandbox.py` ? called_by_detected=yes, lines=32
- `patch_cj_refresh.py` ? called_by_detected=no, lines=44
- `patch_supplier.py` ? called_by_detected=no, lines=17
- `tests/test_supplier_module.py` ? called_by_detected=no, lines=48

### Architecture note
This block maps SKUs to supplier data, CJ payloads, shipping, and purchase queue.

## 3. Pricing and Profit

### Active autopilot steps
- **profit_checked_products** ? MISSING ? `app/profit_checked_products.py`
- **roi_simulation** ? OK ? `app/roi_simulation.py`
- **negative_roi_auto_pause** ? OK ? `app/negative_roi_auto_pause.py`

### Related project files
- `app/ai_pricing_engine.py` ? called_by_detected=no, lines=62
- `app/cleanup_pricing_candidates.py` ? called_by_detected=no, lines=15
- `app/engines/pricing.py` ? called_by_detected=no, lines=94
- `app/finance/advanced_profit_engine.py` ? called_by_detected=yes, lines=116
- `app/margin_engine.py` ? called_by_detected=no, lines=48
- `app/negative_roi_auto_pause.py` ? called_by_detected=yes, lines=32
- `app/patch_negative_roi_runner.py` ? called_by_detected=no, lines=17
- `app/patch_roi_runner.py` ? called_by_detected=no, lines=17
- `app/pricing_ai.py` ? called_by_detected=yes, lines=26
- `app/pricing_apply_safe.py` ? called_by_detected=no, lines=33
- `app/pricing_experiments.py` ? called_by_detected=no, lines=55
- `app/profit_report.py` ? called_by_detected=no, lines=40
- `app/roi_engine.py` ? called_by_detected=no, lines=46
- `app/roi_report.py` ? called_by_detected=no, lines=41
- `app/roi_simulation.py` ? called_by_detected=yes, lines=77
- `app/sales_roi_engine.py` ? called_by_detected=no, lines=103
- `app/services/pricing_agent.py` ? called_by_detected=no, lines=9
- `app/services/profit_engine.py` ? called_by_detected=yes, lines=37
- `app/shopify_automation/pricing.py` ? called_by_detected=yes, lines=47
- `app/shopify_automation/pricing_OK.py` ? called_by_detected=no, lines=47
- `app/shopify_automation/routes_PRICING_OK.py` ? called_by_detected=no, lines=436
- `app/suppliers/pricing.py` ? called_by_detected=yes, lines=12
- `patch_dynamic_pricing_import.py` ? called_by_detected=no, lines=31
- `tests/test_advanced_profit_risk.py` ? called_by_detected=no, lines=115
- `tests/test_profit_and_governor.py` ? called_by_detected=no, lines=60

### Architecture note
This block decides whether the product is profitable and calculates sale price, margin, ROI, and guardrails.

## 4. Listing and Publishing

### Active autopilot steps
- **refresh_ebay_token** ? OK ? `app/refresh_ebay_token.py`
- **shopify_crm_events** ? OK ? `app/shopify_crm_events.py`
- **etsy_connection_status** ? OK ? `app/etsy_connection_status.py`
- **etsy_autopilot** ? OK ? `app/etsy_autopilot.py`
- **publish_execution_plan** ? OK ? `app/publish_execution_plan.py`
- **trend_listing_validator** ? MISSING ? `app/trend_listing_validator.py`
- **auto_publish_or_fallback** ? OK ? `app/auto_publish_or_fallback.py`
- **refresh_shopify_token** ? OK ? `app/refresh_shopify_token.py`
- **listing_publish_execution_plan_real** ? MISSING ? `app/listing_publish_execution_plan_real.py`
- **marketplace_listing_publisher** ? MISSING ? `app/marketplace_listing_publisher.py`
- **draft_listing_activation_plan** ? MISSING ? `app/draft_listing_activation_plan.py`
- **draft_listing_activator** ? MISSING ? `app/draft_listing_activator.py`
- **marketplace_order_autobuy** ? MISSING ? `app/marketplace_order_autobuy.py`

### Related project files
- `app/auto_publish_or_fallback.py` ? called_by_detected=yes, lines=93
- `app/channels/ebay_adapter.py` ? called_by_detected=no, lines=22
- `app/channels/ebay_gateway.py` ? called_by_detected=yes, lines=311
- `app/channels/ebay_gateway_ACCESS_TOKEN_OK.py` ? called_by_detected=no, lines=149
- `app/channels/ebay_gateway_CONNECTED_OK.py` ? called_by_detected=no, lines=149
- `app/channels/ebay_gateway_INVENTORY_ITEM_OK.py` ? called_by_detected=no, lines=193
- `app/channels/etsy_adapter.py` ? called_by_detected=no, lines=22
- `app/channels/shopify_adapter.py` ? called_by_detected=no, lines=287
- `app/channels/shopify_config.py` ? called_by_detected=yes, lines=27
- `app/channels/woocommerce_adapter.py` ? called_by_detected=no, lines=22
- `app/channels/woocommerce_gateway.py` ? called_by_detected=yes, lines=300
- `app/check_ebay_env_safe.py` ? called_by_detected=no, lines=17
- `app/collect_ebay_orders.py` ? called_by_detected=no, lines=71
- `app/collect_shopify_orders.py` ? called_by_detected=no, lines=88
- `app/collect_woocommerce_orders.py` ? called_by_detected=no, lines=98
- `app/commerce/routes_EBAY_CONNECTED_OK.py` ? called_by_detected=no, lines=145
- `app/commerce/routes_EBAY_OVERVIEW_CONNECTED_OK.py` ? called_by_detected=no, lines=146
- `app/daily_publish_guard.py` ? called_by_detected=yes, lines=21
- `app/debug_shopify_crm_source.py` ? called_by_detected=no, lines=30
- `app/debug_shopify_env.py` ? called_by_detected=no, lines=12
- `app/delete_shopify_duplicate.py` ? called_by_detected=no, lines=18
- `app/ebay_read_validation.py` ? called_by_detected=no, lines=75
- `app/ebay_write_offer_validation.py` ? called_by_detected=no, lines=116
- `app/ebay_write_validation.py` ? called_by_detected=no, lines=97
- `app/engines/marketplace.py` ? called_by_detected=no, lines=85
- `app/engines/marketplace_scoring.py` ? called_by_detected=no, lines=99
- `app/engines/publish_registry.py` ? called_by_detected=yes, lines=131
- `app/etsy_auth_url.py` ? called_by_detected=no, lines=35
- `app/etsy_autopilot.py` ? called_by_detected=yes, lines=27
- `app/etsy_connection_status.py` ? called_by_detected=yes, lines=51
- `app/etsy_oauth_exchange.py` ? called_by_detected=no, lines=72
- `app/feeds/meta_shopify_feed.py` ? called_by_detected=yes, lines=89
- `app/final_mvp/shopify.py` ? called_by_detected=yes, lines=56
- `app/fix_woocommerce_validation_url.py` ? called_by_detected=no, lines=12
- `app/generate_publish_queue.py` ? called_by_detected=no, lines=54
- `app/global_marketplace_roadmap.py` ? called_by_detected=no, lines=110
- `app/import_shopify_products.py` ? called_by_detected=no, lines=53
- `app/import_shopify_results.py` ? called_by_detected=no, lines=85
- `app/listing_publish_execution_plan.py` ? called_by_detected=no, lines=39
- `app/listing_publish_validator.py` ? called_by_detected=no, lines=51
- `app/listing_publisher_plan.py` ? called_by_detected=no, lines=42
- `app/listings/__init__.py` ? called_by_detected=no, lines=0
- `app/listings/generator.py` ? called_by_detected=yes, lines=123
- `app/listings/schemas.py` ? called_by_detected=yes, lines=40
- `app/main_STABLE_AI_SHOPIFY_PIPELINE.py` ? called_by_detected=yes, lines=1888
- `app/main_WITH_SHOPIFY_AUTO_MODULE_OK.py` ? called_by_detected=no, lines=1892
- `app/main_WORKING_SHOPIFY_OK.py` ? called_by_detected=no, lines=1719
- `app/main_before_shopify_fallback.py` ? called_by_detected=no, lines=2683
- `app/marketplaces/__init__.py` ? called_by_detected=no, lines=4
- `app/marketplaces/base.py` ? called_by_detected=yes, lines=37
- `app/marketplaces/listing_builder.py` ? called_by_detected=yes, lines=32
- `app/marketplaces/mock_marketplace.py` ? called_by_detected=yes, lines=86
- `app/marketplaces/registry.py` ? called_by_detected=yes, lines=24
- `app/marketplaces/schemas.py` ? called_by_detected=yes, lines=75
- `app/marketplaces/shopify_marketplace.py` ? called_by_detected=yes, lines=139
- `app/one_click_publish_helper.py` ? called_by_detected=no, lines=18
- `app/patch_autopilot_etsy.py` ? called_by_detected=no, lines=16
- `app/patch_autopilot_publish_plan.py` ? called_by_detected=no, lines=14
- `app/patch_autopilot_shopify_refresh.py` ? called_by_detected=no, lines=13
- `app/patch_status_etsy.py` ? called_by_detected=no, lines=22
- `app/publish_dog_socks_with_image.py` ? called_by_detected=no, lines=49
- `app/publish_ebay_from_imports.py` ? called_by_detected=no, lines=131
- `app/publish_ebay_test.py` ? called_by_detected=no, lines=25
- `app/publish_execution_plan.py` ? called_by_detected=yes, lines=36
- `app/refresh_ebay_token.py` ? called_by_detected=yes, lines=51
- `app/refresh_shopify_token.py` ? called_by_detected=yes, lines=121
- `app/services/listing_agent.py` ? called_by_detected=no, lines=27
- `app/services/shopify_client.py` ? called_by_detected=no, lines=23
- `app/shopify_automation/__init__.py` ? called_by_detected=no, lines=1
- `app/shopify_automation/analytics.py` ? called_by_detected=yes, lines=48
- `app/shopify_automation/duplicate_fix.py` ? called_by_detected=no, lines=24
- `app/shopify_automation/orders.py` ? called_by_detected=yes, lines=30
- `app/shopify_automation/orders_OK.py` ? called_by_detected=no, lines=30
- `app/shopify_automation/pricing.py` ? called_by_detected=yes, lines=47
- `app/shopify_automation/pricing_OK.py` ? called_by_detected=no, lines=47
- `app/shopify_automation/routes.py` ? called_by_detected=yes, lines=580
- `app/shopify_automation/routes_ACTIONS_OK.py` ? called_by_detected=no, lines=580
- `app/shopify_automation/routes_DASHBOARD_CARDS_OK.py` ? called_by_detected=no, lines=559
- `app/shopify_automation/routes_DASHBOARD_STATUS_OK.py` ? called_by_detected=no, lines=559
- `app/shopify_automation/routes_PRICING_OK.py` ? called_by_detected=no, lines=436
- ... plus 63 more related files

### Architecture note
This block turns product decisions into channel-specific listings and product feeds.

## 5. Orders

### Active autopilot steps
- **real_sales_collector** ? OK ? `app/real_sales_collector.py`

### Related project files
- `app/autonomous_order_router.py` ? called_by_detected=no, lines=70
- `app/collect_ebay_orders.py` ? called_by_detected=no, lines=71
- `app/collect_incoming_orders.py` ? called_by_detected=no, lines=50
- `app/collect_shopify_orders.py` ? called_by_detected=no, lines=88
- `app/collect_woocommerce_orders.py` ? called_by_detected=no, lines=98
- `app/order_orchestrator.py` ? called_by_detected=no, lines=49
- `app/real_sales_collector.py` ? called_by_detected=yes, lines=201

### Architecture note
This block collects paid customer orders from marketplaces and normalizes them into incoming_orders.json.

## 6. Fulfillment

### Active autopilot steps
- **cj_paid_order_fulfillment** ? MISSING ? `app/cj_paid_order_fulfillment.py`
- **customer_fulfillment_support_status** ? MISSING ? `app/customer_fulfillment_support_status.py`
- **autonomous_fulfillment_status** ? OK ? `app/autonomous_fulfillment_status.py`

### Related project files
- `app/autonomous_fulfillment_status.py` ? called_by_detected=yes, lines=41
- `app/cj_customer_address_validator.py` ? called_by_detected=no, lines=50
- `app/cj_purchase_executor.py` ? called_by_detected=no, lines=67
- `app/fulfillment/__init__.py` ? called_by_detected=no, lines=0
- `app/fulfillment/schemas.py` ? called_by_detected=yes, lines=61
- `app/fulfillment/service.py` ? called_by_detected=yes, lines=120
- `app/fulfillment_guard.py` ? called_by_detected=yes, lines=40
- `app/fulfillment_status_report.py` ? called_by_detected=no, lines=40
- `app/services/fulfillment_agent.py` ? called_by_detected=no, lines=10
- `app/supplier_purchase_queue.py` ? called_by_detected=no, lines=43
- `app/test_fulfillment_guard.py` ? called_by_detected=no, lines=19
- `app/tracking_sync.py` ? called_by_detected=no, lines=35
- `tests/test_fulfillment_agent.py` ? called_by_detected=no, lines=91

### Architecture note
This block should buy from supplier only after paid customer order and only when margin/risk rules pass.

## 7. Marketing and Ads

### Active autopilot steps
- **google_ads_token_refresher** ? OK ? `app/google_ads_token_refresher.py`
- **meta_token_refresh** ? OK ? `app/meta_token_refresh.py`
- **meta_page_token_refresh** ? OK ? `app/meta_page_token_refresh.py`
- **social_content_generator** ? OK ? `app/social_content_generator.py`
- **social_content_enhancer** ? OK ? `app/social_content_enhancer.py`
- **meta_ad_drafts_from_content** ? OK ? `app/meta_ad_drafts_from_content.py`
- **google_ad_drafts_from_content** ? OK ? `app/google_ad_drafts_from_content.py`
- **campaign_hub** ? OK ? `app/campaign_hub.py`
- **campaign_approval_queue** ? OK ? `app/campaign_approval_queue.py`
- **auto_spend_executor** ? OK ? `app/auto_spend_executor.py`
- **negative_roi_auto_pause** ? OK ? `app/negative_roi_auto_pause.py`
- **hourly_budget_monitor** ? OK ? `app/hourly_budget_monitor.py`
- **live_spend_permission_gate** ? OK ? `app/live_spend_permission_gate.py`
- **live_backend_router** ? OK ? `app/live_backend_router.py`
- **meta_live_campaign_builder** ? OK ? `app/meta_live_campaign_builder.py`
- **google_live_campaign_builder** ? OK ? `app/google_live_campaign_builder.py`
- **live_campaign_registry** ? OK ? `app/live_campaign_registry.py`
- **live_api_execution_gate** ? OK ? `app/live_api_execution_gate.py`
- **live_execution_reporter** ? OK ? `app/live_execution_reporter.py`
- **live_mode_final_lock** ? OK ? `app/live_mode_final_lock.py`
- **meta_long_lived_token** ? MISSING ? `app/meta_long_lived_token.py`
- **meta_live_executor** ? OK ? `app/meta_live_executor.py`
- **google_live_executor** ? OK ? `app/google_live_executor.py`
- **live_execution_consolidator** ? OK ? `app/live_execution_consolidator.py`
- **live_spend_audit_ledger** ? OK ? `app/live_spend_audit_ledger.py`
- **live_spend_audit_reader** ? OK ? `app/live_spend_audit_reader.py`

### Related project files
- `app/ad_campaign_executor.py` ? called_by_detected=no, lines=56
- `app/auto_spend_executor.py` ? called_by_detected=yes, lines=51
- `app/budget_controller.py` ? called_by_detected=no, lines=55
- `app/budget_mode_detector.py` ? called_by_detected=no, lines=43
- `app/budget_scaling_rules.py` ? called_by_detected=no, lines=29
- `app/campaign_approval_queue.py` ? called_by_detected=yes, lines=36
- `app/campaign_executor.py` ? called_by_detected=no, lines=64
- `app/campaign_hub.py` ? called_by_detected=yes, lines=47
- `app/channel_live_test.py` ? called_by_detected=no, lines=110
- `app/channels/google_merchant_adapter.py` ? called_by_detected=no, lines=17
- `app/channels/meta_adapter.py` ? called_by_detected=yes, lines=54
- `app/channels/meta_channel.py` ? called_by_detected=yes, lines=24
- `app/channels/meta_shop_adapter.py` ? called_by_detected=no, lines=17
- `app/check_meta_ads.py` ? called_by_detected=no, lines=28
- `app/check_meta_adsets.py` ? called_by_detected=no, lines=29
- `app/feeds/google_merchant_feed.py` ? called_by_detected=no, lines=89
- `app/feeds/meta_feed.py` ? called_by_detected=no, lines=109
- `app/feeds/meta_shopify_feed.py` ? called_by_detected=yes, lines=89
- `app/fix_bom_campaign_queue.py` ? called_by_detected=no, lines=12
- `app/fix_meta_account_id.py` ? called_by_detected=no, lines=22
- `app/fix_meta_budget_sharing.py` ? called_by_detected=no, lines=20
- `app/fix_meta_objective.py` ? called_by_detected=no, lines=14
- `app/fix_meta_special_categories.py` ? called_by_detected=no, lines=13
- `app/google_access_monitor.py` ? called_by_detected=no, lines=52
- `app/google_access_status.py` ? called_by_detected=yes, lines=28
- `app/google_activation_readiness_gate.py` ? called_by_detected=no, lines=55
- `app/google_ad_drafts_from_content.py` ? called_by_detected=yes, lines=39
- `app/google_ads_readiness.py` ? called_by_detected=no, lines=44
- `app/google_ads_token_refresher.py` ? called_by_detected=yes, lines=82
- `app/google_campaign_live_creator.py` ? called_by_detected=no, lines=69
- `app/google_campaign_live_poster.py` ? called_by_detected=no, lines=92
- `app/google_live_campaign_builder.py` ? called_by_detected=yes, lines=38
- `app/google_live_executor.py` ? called_by_detected=yes, lines=66
- `app/google_payload_safe_creator.py` ? called_by_detected=no, lines=38
- `app/google_refresh_token.py` ? called_by_detected=no, lines=61
- `app/hourly_budget_monitor.py` ? called_by_detected=yes, lines=35
- `app/live_api_execution_gate.py` ? called_by_detected=yes, lines=44
- `app/live_backend_router.py` ? called_by_detected=yes, lines=32
- `app/live_campaign_registry.py` ? called_by_detected=yes, lines=49
- `app/live_execution_consolidator.py` ? called_by_detected=yes, lines=51
- `app/live_execution_reporter.py` ? called_by_detected=yes, lines=50
- `app/live_mode_final_lock.py` ? called_by_detected=yes, lines=33
- `app/live_spend_audit_ledger.py` ? called_by_detected=yes, lines=29
- `app/live_spend_audit_reader.py` ? called_by_detected=yes, lines=22
- `app/live_spend_permission_gate.py` ? called_by_detected=yes, lines=38
- `app/meta_activate_ad.py` ? called_by_detected=no, lines=38
- `app/meta_activate_adset.py` ? called_by_detected=no, lines=36
- `app/meta_activate_campaign.py` ? called_by_detected=no, lines=36
- `app/meta_activation_executor.py` ? called_by_detected=no, lines=44
- `app/meta_activation_readiness_gate.py` ? called_by_detected=no, lines=50
- `app/meta_ad_accounts.py` ? called_by_detected=no, lines=53
- `app/meta_ad_builder.py` ? called_by_detected=no, lines=76
- `app/meta_ad_drafts_from_content.py` ? called_by_detected=yes, lines=32
- `app/meta_ads_live_creator.py` ? called_by_detected=no, lines=35
- `app/meta_ads_readiness.py` ? called_by_detected=no, lines=42
- `app/meta_adset_builder.py` ? called_by_detected=no, lines=79
- `app/meta_adset_live_creator.py` ? called_by_detected=no, lines=37
- `app/meta_assets_discovery.py` ? called_by_detected=no, lines=40
- `app/meta_auto_stop_monitor.py` ? called_by_detected=no, lines=40
- `app/meta_business_assets.py` ? called_by_detected=no, lines=48
- `app/meta_business_sync.py` ? called_by_detected=no, lines=30
- `app/meta_campaign_live_creator.py` ? called_by_detected=no, lines=69
- `app/meta_campaign_live_poster.py` ? called_by_detected=no, lines=63
- `app/meta_campaign_registry_sync.py` ? called_by_detected=no, lines=32
- `app/meta_connection_status.py` ? called_by_detected=no, lines=43
- `app/meta_creative_builder.py` ? called_by_detected=no, lines=87
- `app/meta_creative_live_creator.py` ? called_by_detected=no, lines=45
- `app/meta_debug_token.py` ? called_by_detected=no, lines=21
- `app/meta_health.py` ? called_by_detected=no, lines=37
- `app/meta_launch_readiness.py` ? called_by_detected=yes, lines=44
- `app/meta_live_campaign_builder.py` ? called_by_detected=yes, lines=38
- `app/meta_live_executor.py` ? called_by_detected=yes, lines=90
- `app/meta_page_post.py` ? called_by_detected=no, lines=37
- `app/meta_page_token_permissions.py` ? called_by_detected=no, lines=16
- `app/meta_page_token_refresh.py` ? called_by_detected=yes, lines=66
- `app/meta_permission_url.py` ? called_by_detected=no, lines=22
- `app/meta_safe_activation_plan.py` ? called_by_detected=no, lines=48
- `app/meta_test_event.py` ? called_by_detected=no, lines=85
- `app/meta_token_auto_repair.py` ? called_by_detected=no, lines=119
- `app/meta_token_refresh.py` ? called_by_detected=yes, lines=126
- ... plus 36 more related files

### Architecture note
This block creates content, ad drafts, paused live campaigns, and spend controls.

## 8. Reporting and Control

### Active autopilot steps
- **railway_health_check** ? MISSING ? `app/railway_health_check.py`
- **etsy_connection_status** ? OK ? `app/etsy_connection_status.py`
- **system_status_report** ? OK ? `app/system_status_report.py`
- **daily_summary** ? OK ? `app/daily_summary.py`
- **product_guardrails** ? OK ? `app/product_guardrails.py`
- **ceo_dashboard** ? OK ? `app/ceo_dashboard.py`
- **send_daily_summary** ? OK ? `app/send_daily_summary.py`
- **send_telegram_summary** ? OK ? `app/send_telegram_summary.py`
- **customer_fulfillment_support_status** ? MISSING ? `app/customer_fulfillment_support_status.py`
- **autonomous_fulfillment_status** ? OK ? `app/autonomous_fulfillment_status.py`

### Related project files
- `app/aliexpress_connection_status.py` ? called_by_detected=no, lines=22
- `app/amazon_connection_status.py` ? called_by_detected=yes, lines=35
- `app/autonomous_fulfillment_status.py` ? called_by_detected=yes, lines=41
- `app/autonomous_loop_health.py` ? called_by_detected=no, lines=58
- `app/ceo_dashboard.py` ? called_by_detected=yes, lines=72
- `app/channel_health.py` ? called_by_detected=yes, lines=96
- `app/channel_health_report.py` ? called_by_detected=yes, lines=36
- `app/check_cj_status.py` ? called_by_detected=no, lines=7
- `app/crm_health_check.py` ? called_by_detected=no, lines=43
- `app/crm_send_guard.py` ? called_by_detected=no, lines=29
- `app/daily_publish_guard.py` ? called_by_detected=yes, lines=21
- `app/daily_summary.py` ? called_by_detected=yes, lines=49
- `app/dashboard/__init__.py` ? called_by_detected=no, lines=1
- `app/dashboard/schemas.py` ? called_by_detected=yes, lines=27
- `app/dashboard/service.py` ? called_by_detected=yes, lines=66
- `app/dashboard_report.py` ? called_by_detected=no, lines=53
- `app/engines/guard.py` ? called_by_detected=no, lines=64
- `app/engines/risk_guard.py` ? called_by_detected=no, lines=51
- `app/etsy_connection_status.py` ? called_by_detected=yes, lines=51
- `app/fulfillment_guard.py` ? called_by_detected=yes, lines=40
- `app/fulfillment_status_report.py` ? called_by_detected=no, lines=40
- `app/global_channel_status_summary.py` ? called_by_detected=no, lines=49
- `app/google_access_status.py` ? called_by_detected=yes, lines=28
- `app/health_check.py` ? called_by_detected=no, lines=41
- `app/inventory_sync_guard.py` ? called_by_detected=no, lines=44
- `app/main_CATALOG_HEALTH_OK.py` ? called_by_detected=no, lines=1888
- `app/main_DASHBOARD_WORKING_OK.py` ? called_by_detected=no, lines=1892
- `app/master_system_health.py` ? called_by_detected=yes, lines=70
- `app/meta_connection_status.py` ? called_by_detected=no, lines=43
- `app/meta_health.py` ? called_by_detected=no, lines=37
- `app/niche_exclusion_guard.py` ? called_by_detected=no, lines=52
- `app/paid_ads_status.py` ? called_by_detected=no, lines=39
- `app/patch_autopilot_system_status.py` ? called_by_detected=no, lines=14
- `app/patch_ceo_dashboard_runner.py` ? called_by_detected=no, lines=17
- `app/patch_daily_summary_priority.py` ? called_by_detected=no, lines=31
- `app/patch_guardrails_runner.py` ? called_by_detected=no, lines=17
- `app/patch_pre_guard_planning.py` ? called_by_detected=no, lines=19
- `app/patch_send_daily_summary.py` ? called_by_detected=no, lines=16
- `app/patch_status_action_executor.py` ? called_by_detected=no, lines=25
- `app/patch_status_etsy.py` ? called_by_detected=no, lines=22
- `app/patch_telegram_summary.py` ? called_by_detected=no, lines=15
- `app/product_guardrails.py` ? called_by_detected=yes, lines=55
- `app/product_image_sync_status.py` ? called_by_detected=no, lines=28
- `app/quick_status.py` ? called_by_detected=no, lines=40
- `app/real_sales_loop_status.py` ? called_by_detected=no, lines=64
- `app/send_daily_summary.py` ? called_by_detected=yes, lines=58
- `app/send_telegram_alert.py` ? called_by_detected=yes, lines=29
- `app/send_telegram_summary.py` ? called_by_detected=yes, lines=60
- `app/shopify_automation/routes_DASHBOARD_CARDS_OK.py` ? called_by_detected=no, lines=559
- `app/shopify_automation/routes_DASHBOARD_STATUS_OK.py` ? called_by_detected=no, lines=559
- `app/status_report.py` ? called_by_detected=no, lines=36
- `app/system_health_dashboard.py` ? called_by_detected=no, lines=58
- `app/system_status_dashboard.py` ? called_by_detected=no, lines=39
- `app/system_status_report.py` ? called_by_detected=yes, lines=94
- `app/telegram_test.py` ? called_by_detected=no, lines=27
- `app/test_fulfillment_guard.py` ? called_by_detected=no, lines=19
- `app/tiktok_connection_status.py` ? called_by_detected=no, lines=54
- `app/woocommerce_live_publish_guard.py` ? called_by_detected=no, lines=29
- `tests/test_admin_dashboard.py` ? called_by_detected=no, lines=39

### Architecture note
This block explains system state through dashboard, daily summary, CEO dashboard, Telegram, and status files.

## Critical missing business links

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

## Recommended target flow

1. Product Discovery finds candidates.
2. Supplier Intelligence resolves supplier cost, shipping, stock, supplier IDs and CJ mapping.
3. Pricing and Profit calculates profitable sale price per marketplace.
4. Listing and Publishing creates listings/drafts on Shopify, Etsy, eBay, WooCommerce, Amazon.
5. Orders collects only paid customer orders.
6. Fulfillment creates supplier purchase queue only after payment and profit recheck.
7. Supplier purchase runs in DRY_RUN until explicitly enabled.
8. Tracking sync updates customer marketplace orders.
9. Marketing promotes winners through Meta/Google while spend guardrails remain active.
10. Reporting explains every action through dashboard, logs and Telegram.