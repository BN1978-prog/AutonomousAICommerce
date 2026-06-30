# AICommerce Data Flow Architecture Book

Created at: 2026-06-29T20:52:35.394857+00:00
Python files scanned: 721
Log/data files detected: 319

## Most central data nodes

### `app/logs/imported_skus.json`
- Writers: 67
  - `app/add_created_at_to_skus.py`
  - `app/arbitrage_safety_gate.py`
  - `app/auto_disable_skus.py`
  - `app/autonomous_loop_health.py`
  - `app/channel_validation.py`
  - `app/click_tracking_init.py`
  - `app/conversion_watch.py`
  - `app/disable_candidates.py`
- Readers: 74
  - `app/add_created_at_to_skus.py`
  - `app/arbitrage_safety_gate.py`
  - `app/auto_disable_skus.py`
  - `app/autonomous_loop_health.py`
  - `app/channel_health_report.py`
  - `app/channel_validation.py`
  - `app/click_tracking_init.py`
  - `app/conversion_watch.py`

### `app/logs/system_status_dashboard.json`
- Writers: 16
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/backup_manager.py`
  - `app/budget_controller.py`
  - `app/conversion_tracking_validation.py`
  - `app/daily_report.py`
  - `app/deployment_readiness_checklist.py`
  - `app/google_activation_readiness_gate.py`
- Readers: 16
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/budget_controller.py`
  - `app/conversion_tracking_validation.py`
  - `app/daily_report.py`
  - `app/deployment_readiness_checklist.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`

### `app/logs/product_performance.json`
- Writers: 12
  - `app/add_product_results.py`
  - `app/apply_scale_limits.py`
  - `app/build_priority_queue.py`
  - `app/clean_catalog.py`
  - `app/daily_summary.py`
  - `app/decision_engine.py`
  - `app/exploration_engine_v2.py`
  - `app/import_shopify_results.py`
- Readers: 13
  - `app/add_product_results.py`
  - `app/apply_scale_limits.py`
  - `app/autopilot_report.py`
  - `app/build_priority_queue.py`
  - `app/clean_catalog.py`
  - `app/daily_summary.py`
  - `app/decision_engine.py`
  - `app/exploration_engine_v2.py`

### `app/logs/real_sales_mode.json`
- Writers: 11
  - `app/budget_controller.py`
  - `app/channel_live_test.py`
  - `app/crm_event_router.py`
  - `app/customer_analytics.py`
  - `app/daily_report.py`
  - `app/global_commerce_control_panel.py`
  - `app/meta_auto_stop_monitor.py`
  - `app/real_sales_loop_status.py`
- Readers: 11
  - `app/budget_controller.py`
  - `app/channel_live_test.py`
  - `app/crm_event_router.py`
  - `app/customer_analytics.py`
  - `app/daily_report.py`
  - `app/global_commerce_control_panel.py`
  - `app/meta_auto_stop_monitor.py`
  - `app/real_sales_loop_status.py`

### `app/logs/crm_send_guard.json`
- Writers: 9
  - `app/crm_confirm_owner_for_test.py`
  - `app/crm_draft_outbox.py`
  - `app/crm_executor_dry_run.py`
  - `app/crm_final_gate.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_queue_builder.py`
  - `app/crm_readiness_summary.py`
- Readers: 9
  - `app/crm_confirm_owner_for_test.py`
  - `app/crm_draft_outbox.py`
  - `app/crm_executor_dry_run.py`
  - `app/crm_final_gate.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_queue_builder.py`
  - `app/crm_readiness_summary.py`

### `app/logs/crm_queue.json`
- Writers: 8
  - `app/crm_executor_dry_run.py`
  - `app/crm_final_gate.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_prepare_single_test.py`
  - `app/crm_queue_builder.py`
  - `app/crm_readiness_summary.py`
  - `app/crm_send_one_test.py`
- Readers: 7
  - `app/crm_executor_dry_run.py`
  - `app/crm_final_gate.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_queue_builder.py`
  - `app/crm_readiness_summary.py`
  - `app/crm_send_one_test.py`

### `app/logs/global_commerce_control_panel.json`
- Writers: 8
  - `app/backup_manager.py`
  - `app/budget_controller.py`
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/global_commerce_control_panel.py`
  - `app/meta_safe_activation_plan.py`
  - `app/production_readiness_report.py`
  - `app/system_status_dashboard.py`
- Readers: 7
  - `app/budget_controller.py`
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/global_commerce_control_panel.py`
  - `app/meta_safe_activation_plan.py`
  - `app/production_readiness_report.py`
  - `app/system_status_dashboard.py`

### `app/logs/master_system_health.json`
- Writers: 6
  - `app/deployment_readiness_checklist.py`
  - `app/deployment_summary.py`
  - `app/master_system_health.py`
  - `app/stable_release_105.py`
  - `app/system_release_marker.py`
  - `app/system_status_report.py`
- Readers: 7
  - `app/deployment_readiness_checklist.py`
  - `app/deployment_summary.py`
  - `app/master_system_health.py`
  - `app/quick_status.py`
  - `app/stable_release_105.py`
  - `app/system_release_marker.py`
  - `app/system_status_report.py`

### `app/logs/supplier_purchase_queue.json`
- Writers: 7
  - `app/autonomous_fulfillment_status.py`
  - `app/autonomous_order_router.py`
  - `app/cj_order_draft_creator.py`
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_executor.py`
  - `app/supplier_purchase_queue.py`
- Readers: 6
  - `app/autonomous_order_router.py`
  - `app/cj_order_draft_creator.py`
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_executor.py`
  - `app/supplier_purchase_queue.py`

### `app/logs/daily_summary.txt`
- Writers: 6
  - `app/auto_scaling_score.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/product_guardrails.py`
  - `app/send_daily_summary.py`
  - `app/send_telegram_summary.py`
- Readers: 6
  - `app/auto_scaling_score.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/product_guardrails.py`
  - `app/send_daily_summary.py`
  - `app/send_telegram_summary.py`

### `app/logs/meta_campaign_registry.json`
- Writers: 6
  - `app/external_platform_blockers.py`
  - `app/meta_adset_live_creator.py`
  - `app/meta_campaign_registry_sync.py`
  - `app/meta_launch_readiness.py`
  - `app/meta_safe_activation_plan.py`
  - `app/sync_meta_campaign_registry.py`
- Readers: 6
  - `app/external_platform_blockers.py`
  - `app/meta_adset_live_creator.py`
  - `app/meta_campaign_registry_sync.py`
  - `app/meta_launch_readiness.py`
  - `app/meta_safe_activation_plan.py`
  - `app/sync_meta_campaign_registry.py`

### `app/logs/crm_channel_readiness.json`
- Writers: 6
  - `app/crm_channel_readiness.py`
  - `app/crm_draft_outbox.py`
  - `app/crm_executor_dry_run.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_readiness_summary.py`
- Readers: 5
  - `app/crm_draft_outbox.py`
  - `app/crm_executor_dry_run.py`
  - `app/crm_health_check.py`
  - `app/crm_orchestrator.py`
  - `app/crm_readiness_summary.py`

### `app/logs/external_blockers_monitor.json`
- Writers: 6
  - `app/alerts_engine.py`
  - `app/backup_manager.py`
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/google_activation_readiness_gate.py`
  - `app/system_status_dashboard.py`
- Readers: 5
  - `app/alerts_engine.py`
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/google_activation_readiness_gate.py`
  - `app/system_status_dashboard.py`

### `app/logs/pricing_experiments.json`
- Writers: 5
  - `app/cleanup_pricing_candidates.py`
  - `app/daily_decision_report.py`
  - `app/pricing_apply_safe.py`
  - `app/pricing_experiments.py`
  - `app/traffic_execution_plan.py`
- Readers: 6
  - `app/cleanup_pricing_candidates.py`
  - `app/daily_decision_report.py`
  - `app/final_system_check.py`
  - `app/pricing_apply_safe.py`
  - `app/pricing_experiments.py`
  - `app/traffic_execution_plan.py`

### `app/logs/promotion_candidates.json`
- Writers: 5
  - `app/pricing_experiments.py`
  - `app/promotion_actions.py`
  - `app/promotion_candidates.py`
  - `app/seo_action_report.py`
  - `app/traffic_brain.py`
- Readers: 6
  - `app/final_system_check.py`
  - `app/pricing_experiments.py`
  - `app/promotion_actions.py`
  - `app/promotion_candidates.py`
  - `app/seo_action_report.py`
  - `app/traffic_brain.py`

### `app/logs/auto_spend_executor.json`
- Writers: 5
  - `app/auto_spend_executor.py`
  - `app/emergency_stop_validator.py`
  - `app/hourly_budget_monitor.py`
  - `app/live_spend_permission_gate.py`
  - `app/spend_history_tracker.py`
- Readers: 5
  - `app/auto_spend_executor.py`
  - `app/emergency_stop_validator.py`
  - `app/hourly_budget_monitor.py`
  - `app/live_spend_permission_gate.py`
  - `app/spend_history_tracker.py`

### `app/logs/autopilot_priority_queue.json`
- Writers: 5
  - `app/build_priority_queue.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/publish_execution_plan.py`
  - `app/system_status_report.py`
- Readers: 5
  - `app/build_priority_queue.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/publish_execution_plan.py`
  - `app/system_status_report.py`

### `app/logs/budget_controller.json`
- Writers: 5
  - `app/budget_controller.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`
  - `app/roi_engine.py`
- Readers: 5
  - `app/budget_controller.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`
  - `app/roi_engine.py`

### `app/logs/google_campaign_live_creator.json`
- Writers: 5
  - `app/google_activation_readiness_gate.py`
  - `app/google_campaign_live_creator.py`
  - `app/google_campaign_live_poster.py`
  - `app/google_payload_safe_creator.py`
  - `app/system_status_report.py`
- Readers: 5
  - `app/google_activation_readiness_gate.py`
  - `app/google_campaign_live_creator.py`
  - `app/google_campaign_live_poster.py`
  - `app/google_payload_safe_creator.py`
  - `app/system_status_report.py`

### `app/logs/incoming_orders.json`
- Writers: 5
  - `app/autonomous_order_router.py`
  - `app/clear_test_orders.py`
  - `app/collect_incoming_orders.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_queue.py`
- Readers: 5
  - `app/autonomous_order_router.py`
  - `app/clear_test_orders.py`
  - `app/collect_incoming_orders.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_queue.py`

### `app/logs/product_catalog.json`
- Writers: 5
  - `app/clean_catalog.py`
  - `app/expand_catalog.py`
  - `app/import_shopify_products.py`
  - `app/smart_generate_publish_queue.py`
  - `app/sync_catalog_performance.py`
- Readers: 5
  - `app/clean_catalog.py`
  - `app/expand_catalog.py`
  - `app/import_shopify_products.py`
  - `app/smart_generate_publish_queue.py`
  - `app/sync_catalog_performance.py`

### `app/logs/product_quality_filter.json`
- Writers: 5
  - `app/compliance_layer.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`
  - `app/product_quality_filter.py`
- Readers: 5
  - `app/compliance_layer.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`
  - `app/product_quality_filter.py`

### `app/logs/crm_final_gate.json`
- Writers: 4
  - `app/crm_final_gate.py`
  - `app/crm_send_one_test.py`
  - `app/deployment_readiness_checklist.py`
  - `app/master_system_health.py`
- Readers: 5
  - `app/crm_final_gate.py`
  - `app/crm_send_one_test.py`
  - `app/deployment_readiness_checklist.py`
  - `app/master_system_health.py`
  - `app/quick_status.py`

### `app/logs/niche_exclusion_summary.json`
- Writers: 4
  - `app/deployment_readiness_checklist.py`
  - `app/master_system_health.py`
  - `app/niche_exclusion_summary.py`
  - `app/system_release_marker.py`
- Readers: 5
  - `app/deployment_readiness_checklist.py`
  - `app/master_system_health.py`
  - `app/niche_exclusion_summary.py`
  - `app/quick_status.py`
  - `app/system_release_marker.py`

### `app/logs/priority_publish_queue.txt`
- Writers: 5
  - `app/auto_publish_or_fallback.py`
  - `app/generate_publish_queue.py`
  - `app/one_click_publish_helper.py`
  - `app/smart_generate_publish_queue.py`
  - `app/traffic_priority_plan.py`
- Readers: 4
  - `app/auto_publish_or_fallback.py`
  - `app/one_click_publish_helper.py`
  - `app/smart_generate_publish_queue.py`
  - `app/traffic_priority_plan.py`

### `app/logs/production_readiness_report.json`
- Writers: 5
  - `app/backup_manager.py`
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/production_readiness_report.py`
  - `app/system_status_dashboard.py`
- Readers: 4
  - `app/daily_report.py`
  - `app/external_blockers_monitor.py`
  - `app/production_readiness_report.py`
  - `app/system_status_dashboard.py`

### `app/logs/recovery_report.json`
- Writers: 5
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/backup_manager.py`
  - `app/master_system_health.py`
  - `app/recovery_layer.py`
- Readers: 4
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/master_system_health.py`
  - `app/recovery_layer.py`

### `app/logs/ad_campaign_executor.json`
- Writers: 4
  - `app/ad_campaign_executor.py`
  - `app/global_commerce_control_panel.py`
  - `app/google_campaign_live_creator.py`
  - `app/meta_campaign_live_creator.py`
- Readers: 4
  - `app/ad_campaign_executor.py`
  - `app/global_commerce_control_panel.py`
  - `app/google_campaign_live_creator.py`
  - `app/meta_campaign_live_creator.py`

### `app/logs/alerts.json`
- Writers: 4
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/backup_manager.py`
  - `app/master_system_health.py`
- Readers: 4
  - `app/alerts_engine.py`
  - `app/autopilot_schedule_readiness.py`
  - `app/master_system_health.py`
  - `app/quick_status.py`

### `app/logs/autopilot_decisions.json`
- Writers: 4
  - `app/apply_scale_limits.py`
  - `app/decision_engine.py`
  - `app/exploration_engine.py`
  - `app/smart_generate_publish_queue.py`
- Readers: 4
  - `app/apply_scale_limits.py`
  - `app/decision_engine.py`
  - `app/exploration_engine.py`
  - `app/smart_generate_publish_queue.py`

### `app/logs/campaign_executor.json`
- Writers: 4
  - `app/ad_campaign_executor.py`
  - `app/campaign_executor.py`
  - `app/google_payload_safe_creator.py`
  - `app/sync_meta_campaign_registry.py`
- Readers: 4
  - `app/ad_campaign_executor.py`
  - `app/campaign_executor.py`
  - `app/google_payload_safe_creator.py`
  - `app/sync_meta_campaign_registry.py`

### `app/logs/compliance_layer.json`
- Writers: 4
  - `app/compliance_layer.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`
- Readers: 4
  - `app/compliance_layer.py`
  - `app/google_activation_readiness_gate.py`
  - `app/master_system_health.py`
  - `app/meta_activation_readiness_gate.py`

### `app/logs/global_arbitrage_engine.json`
- Writers: 4
  - `app/ai_pricing_engine.py`
  - `app/compliance_layer.py`
  - `app/inventory_sync_guard.py`
  - `app/product_quality_filter.py`
- Readers: 4
  - `app/ai_pricing_engine.py`
  - `app/compliance_layer.py`
  - `app/inventory_sync_guard.py`
  - `app/product_quality_filter.py`

### `app/logs/meta_launch_readiness.json`
- Writers: 4
  - `app/global_commerce_control_panel.py`
  - `app/meta_launch_readiness.py`
  - `app/production_readiness_report.py`
  - `app/system_status_report.py`
- Readers: 4
  - `app/global_commerce_control_panel.py`
  - `app/meta_launch_readiness.py`
  - `app/production_readiness_report.py`
  - `app/system_status_report.py`

### `app/logs/opportunities/global_execution_plan.json`
- Writers: 4
  - `app/global_commerce_control_panel.py`
  - `app/global_execution_plan.py`
  - `app/meta_creative_live_creator.py`
  - `app/real_traffic_launcher.py`
- Readers: 4
  - `app/global_commerce_control_panel.py`
  - `app/global_execution_plan.py`
  - `app/meta_creative_live_creator.py`
  - `app/real_traffic_launcher.py`

### `app/logs/paid_ads_status.json`
- Writers: 4
  - `app/channel_live_test.py`
  - `app/paid_ads_status.py`
  - `app/traffic_mode.py`
  - `app/traffic_readiness.py`
- Readers: 4
  - `app/channel_live_test.py`
  - `app/paid_ads_status.py`
  - `app/traffic_mode.py`
  - `app/traffic_readiness.py`

### `app/logs/social_content_enhanced.json`
- Writers: 4
  - `app/campaign_hub.py`
  - `app/google_ad_drafts_from_content.py`
  - `app/meta_ad_drafts_from_content.py`
  - `app/social_content_enhancer.py`
- Readers: 4
  - `app/campaign_hub.py`
  - `app/google_ad_drafts_from_content.py`
  - `app/meta_ad_drafts_from_content.py`
  - `app/social_content_enhancer.py`

### `app/logs/supplier_fallback_engine.json`
- Writers: 4
  - `app/deployment_readiness_checklist.py`
  - `app/inventory_sync_guard.py`
  - `app/master_system_health.py`
  - `app/supplier_fallback_engine.py`
- Readers: 4
  - `app/deployment_readiness_checklist.py`
  - `app/inventory_sync_guard.py`
  - `app/master_system_health.py`
  - `app/supplier_fallback_engine.py`

### `app/logs/tracking_updates.json`
- Writers: 4
  - `app/add_test_tracking.py`
  - `app/fulfillment_status_report.py`
  - `app/push_tracking_to_channels.py`
  - `app/tracking_sync.py`
- Readers: 4
  - `app/add_test_tracking.py`
  - `app/fulfillment_status_report.py`
  - `app/push_tracking_to_channels.py`
  - `app/tracking_sync.py`

### `app/logs/crm_message_generator.json`
- Writers: 4
  - `app/crm_draft_outbox.py`
  - `app/crm_health_check.py`
  - `app/crm_message_generator.py`
  - `app/crm_send_guard.py`
- Readers: 3
  - `app/crm_draft_outbox.py`
  - `app/crm_health_check.py`
  - `app/crm_send_guard.py`

## Logs with no detected writer


## Logs with no detected reader

- `app/logs/aliexpress_connection_status.json` written by 1 file(s)
- `app/logs/autonomous_fulfillment_status.json` written by 1 file(s)
- `app/logs/budget_scaling_rules.json` written by 1 file(s)
- `app/logs/cj_product_detail.json` written by 1 file(s)
- `app/logs/cj_product_search.json` written by 1 file(s)
- `app/logs/crm_owner_confirmed.json` written by 1 file(s)
- `app/logs/crm_provider_config_check.json` written by 1 file(s)
- `app/logs/full_system_final_run.json` written by 1 file(s)
- `app/logs/google_access_status.json` written by 1 file(s)
- `app/logs/manual_social_publish_log.json` written by 1 file(s)
- `app/logs/meta_page_post_result.json` written by 1 file(s)
- `app/logs/pipeline_runner_results.json` written by 1 file(s)
- `app/logs/post_to_copy.txt` written by 1 file(s)
- `app/logs/refund_dispute_engine.json` written by 1 file(s)
- `app/logs/sales_mode.json` written by 1 file(s)
- `app/logs/shopify_order_addresses.json` written by 1 file(s)
- `app/logs/social_links_to_use.txt` written by 1 file(s)
- `app/logs/system_maintenance_planner.json` written by 1 file(s)
- `app/logs/tiktok_connection_status.json` written by 1 file(s)
- `app/logs/traffic_prelaunch.json` written by 1 file(s)
- `app/logs/utm_social_links.json` written by 1 file(s)
- `app/logs/woocommerce_category_fix_result.json` written by 1 file(s)
- `app/logs/woocommerce_draft_enrichment_result.json` written by 1 file(s)
- `app/logs/woocommerce_draft_publish_result.json` written by 1 file(s)
- `app/logs/woocommerce_image_auto_upload_report.json` written by 1 file(s)
- `app/logs/woocommerce_image_gap_report.json` written by 1 file(s)
- `app/logs/woocommerce_image_manual_action.json` written by 1 file(s)
- `app/logs/woocommerce_local_image_upload.json` written by 1 file(s)
- `app/logs/woocommerce_order_monitor.json` written by 1 file(s)
- `app/logs/woocommerce_placeholder_images.json` written by 1 file(s)
- `app/logs/woocommerce_pre_publish_check.json` written by 1 file(s)
- `app/logs/woocommerce_publish_result.json` written by 1 file(s)

## Critical business-flow logs

### `app/logs/exploration_v2.json`
- Writers:
  - `app/build_priority_queue.py`
  - `app/exploration_engine_v2.py`
  - `app/patch_report_exploration_v2.py`
- Readers:
  - `app/autopilot_report.py`
  - `app/build_priority_queue.py`
  - `app/exploration_engine_v2.py`
  - `app/patch_report_exploration_v2.py`

### `app/logs/autopilot_priority_queue.json`
- Writers:
  - `app/build_priority_queue.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/publish_execution_plan.py`
  - `app/system_status_report.py`
- Readers:
  - `app/build_priority_queue.py`
  - `app/daily_summary.py`
  - `app/patch_daily_summary_priority.py`
  - `app/publish_execution_plan.py`
  - `app/system_status_report.py`

### `app/logs/publish_execution_plan.json`
- Writers:
  - `app/action_executor.py`
  - `app/publish_execution_plan.py`
  - `app/social_content_generator.py`
- Readers:
  - `app/action_executor.py`
  - `app/publish_execution_plan.py`
  - `app/social_content_generator.py`

### `app/logs/imported_skus.json`
- Writers:
  - `app/add_created_at_to_skus.py`
  - `app/arbitrage_safety_gate.py`
  - `app/auto_disable_skus.py`
  - `app/autonomous_loop_health.py`
  - `app/channel_validation.py`
  - `app/click_tracking_init.py`
  - `app/conversion_watch.py`
  - `app/disable_candidates.py`
  - `app/dynamic_product_score.py`
  - `app/dynamic_score_sync.py`
  - `app/ebay_read_validation.py`
  - `app/ebay_write_offer_validation.py`
  - `app/ebay_write_validation.py`
  - `app/feed_channel_validation.py`
  - `app/feed_mass_regenerator.py`
  - `app/feed_regenerator.py`
  - `app/hunter_action_executor.py`
  - `app/hunter_action_plan.py`
  - `app/hunter_import.py`
  - `app/hunter_registry_sync.py`
  - `app/main.py`
  - `app/main_AUTOPILOT_NO_DUPES_OK.py`
  - `app/main_AUTOPILOT_SAFE_FLOW_OK.py`
  - `app/main_CATALOG_HEALTH_OK.py`
  - `app/main_CLEAN_CATALOG_OK.py`
  - `app/main_DASHBOARD_WORKING_OK.py`
  - `app/main_SAFE_FLOW_OK.py`
  - `app/main_STABLE_AI_SHOPIFY_PIPELINE.py`
  - `app/main_WITH_SHOPIFY_AUTO_MODULE_OK.py`
  - `app/main_WORKING_DEDUPE_OK.py`
  - `app/main_WORKING_SHOPIFY_OK.py`
  - `app/main_backup.py`
  - `app/main_before_shopify_fallback.py`
  - `app/main_broken_20260518_112242.py`
  - `app/market_arbitrage_engine.py`
  - `app/no_sales_report.py`
  - `app/order_orchestrator.py`
  - `app/performance_board.py`
  - `app/promotion_candidates.py`
  - `app/publish_ebay_from_imports.py`
  - `app/real_sales_collector.py`
  - `app/registry_push_sync.py`
  - `app/registry_quality_report.py`
  - `app/roi_report.py`
  - `app/sales_roi_engine.py`
  - `app/seo_action_report.py`
  - `app/seo_auto_apply.py`
  - `app/seo_generate_full.py`
  - `app/seo_mass_apply.py`
  - `app/seo_mass_push_plan.py`
  - `app/seo_pipeline_audit.py`
  - `app/seo_push_to_channels.py`
  - `app/seo_quality_fix.py`
  - `app/seo_quality_score.py`
  - `app/seo_repush_required.py`
  - `app/shopify_registry_hydrator.py`
  - `app/shopify_write_validation.py`
  - `app/supplier_purchase_queue.py`
  - `app/sync_ebay_orders.py`
  - `app/sync_hunter_to_shopify.py`
  - `app/sync_shopify_orders.py`
  - `app/system_health_dashboard.py`
  - `app/tier_strategy_apply.py`
  - `app/tier_summary.py`
  - `app/update_shopify_existing.py`
  - `backfill_ebay_metadata.py`
  - `clean_mock_logs.py`
- Readers:
  - `app/add_created_at_to_skus.py`
  - `app/arbitrage_safety_gate.py`
  - `app/auto_disable_skus.py`
  - `app/autonomous_loop_health.py`
  - `app/channel_health_report.py`
  - `app/channel_validation.py`
  - `app/click_tracking_init.py`
  - `app/conversion_watch.py`
  - `app/debug_pipeline.py`
  - `app/disable_candidates.py`
  - `app/dynamic_product_score.py`
  - `app/dynamic_score_sync.py`
  - `app/ebay_read_validation.py`
  - `app/ebay_write_offer_validation.py`
  - `app/ebay_write_validation.py`
  - `app/feed_channel_validation.py`
  - `app/feed_mass_regenerator.py`
  - `app/feed_regenerator.py`
  - `app/feeds/google_merchant_feed.py`
  - `app/feeds/meta_shopify_feed.py`
  - `app/final_system_check.py`
  - `app/hunter_action_executor.py`
  - `app/hunter_action_plan.py`
  - `app/hunter_import.py`
  - `app/hunter_registry_sync.py`
  - `app/main.py`
  - `app/main_AUTOPILOT_NO_DUPES_OK.py`
  - `app/main_AUTOPILOT_SAFE_FLOW_OK.py`
  - `app/main_CATALOG_HEALTH_OK.py`
  - `app/main_CLEAN_CATALOG_OK.py`
  - `app/main_DASHBOARD_WORKING_OK.py`
  - `app/main_SAFE_FLOW_OK.py`
  - `app/main_STABLE_AI_SHOPIFY_PIPELINE.py`
  - `app/main_WITH_SHOPIFY_AUTO_MODULE_OK.py`
  - `app/main_WORKING_DEDUPE_OK.py`
  - `app/main_WORKING_SHOPIFY_OK.py`
  - `app/main_backup.py`
  - `app/main_before_shopify_fallback.py`
  - `app/main_broken_20260518_112242.py`
  - `app/market_arbitrage_engine.py`
  - `app/no_sales_report.py`
  - `app/order_orchestrator.py`
  - `app/performance_board.py`
  - `app/pipeline_summary.py`
  - `app/promotion_candidates.py`
  - `app/publish_ebay_from_imports.py`
  - `app/real_sales_collector.py`
  - `app/registry_inspector.py`
  - `app/registry_push_sync.py`
  - `app/registry_quality_report.py`
  - `app/roi_report.py`
  - `app/sales_roi_engine.py`
  - `app/seo_action_report.py`
  - `app/seo_auto_apply.py`
  - `app/seo_generate_full.py`
  - `app/seo_mass_apply.py`
  - `app/seo_mass_push_plan.py`
  - `app/seo_pipeline_audit.py`
  - `app/seo_push_to_channels.py`
  - `app/seo_quality_fix.py`
  - `app/seo_quality_score.py`
  - `app/seo_repush_required.py`
  - `app/shopify_registry_hydrator.py`
  - `app/shopify_write_validation.py`
  - `app/supplier_purchase_queue.py`
  - `app/sync_ebay_orders.py`
  - `app/sync_hunter_to_shopify.py`
  - `app/sync_shopify_orders.py`
  - `app/system_health_dashboard.py`
  - `app/tier_strategy_apply.py`
  - `app/tier_summary.py`
  - `app/update_shopify_existing.py`
  - `backfill_ebay_metadata.py`
  - `clean_mock_logs.py`

### `app/logs/shopify_orders.json`
- Writers:
  - `app/collect_incoming_orders.py`
  - `app/collect_shopify_orders.py`
- Readers:
  - `app/collect_incoming_orders.py`

### `app/logs/ebay_orders.json`
- Writers:
  - `app/collect_ebay_orders.py`
  - `app/collect_incoming_orders.py`
- Readers:
  - `app/collect_incoming_orders.py`

### `app/logs/woocommerce_orders.json`
- Writers:
  - `app/collect_incoming_orders.py`
  - `app/collect_woocommerce_orders.py`
- Readers:
  - `app/collect_incoming_orders.py`

### `app/logs/incoming_orders.json`
- Writers:
  - `app/autonomous_order_router.py`
  - `app/clear_test_orders.py`
  - `app/collect_incoming_orders.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_queue.py`
- Readers:
  - `app/autonomous_order_router.py`
  - `app/clear_test_orders.py`
  - `app/collect_incoming_orders.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_queue.py`

### `app/logs/supplier_purchase_queue.json`
- Writers:
  - `app/autonomous_fulfillment_status.py`
  - `app/autonomous_order_router.py`
  - `app/cj_order_draft_creator.py`
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_executor.py`
  - `app/supplier_purchase_queue.py`
- Readers:
  - `app/autonomous_order_router.py`
  - `app/cj_order_draft_creator.py`
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/supplier_purchase_executor.py`
  - `app/supplier_purchase_queue.py`

### `app/logs/cj_order_drafts.json`
- Writers:
  - `app/cj_order_draft_creator.py`
  - `app/cj_payload_builder.py`
  - `app/real_sales_loop_status.py`
- Readers:
  - `app/cj_order_draft_creator.py`
  - `app/cj_payload_builder.py`
  - `app/real_sales_loop_status.py`

### `app/logs/cj_order_payloads.json`
- Writers:
  - `app/cj_customer_address_validator.py`
  - `app/cj_payload_builder.py`
  - `app/real_sales_loop_status.py`
- Readers:
  - `app/cj_customer_address_validator.py`
  - `app/cj_payload_builder.py`
  - `app/real_sales_loop_status.py`

### `app/logs/cj_purchase_attempts.json`
- Writers:
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/tracking_sync.py`
- Readers:
  - `app/cj_purchase_executor.py`
  - `app/fulfillment_status_report.py`
  - `app/tracking_sync.py`

### `app/logs/tracking_updates.json`
- Writers:
  - `app/add_test_tracking.py`
  - `app/fulfillment_status_report.py`
  - `app/push_tracking_to_channels.py`
  - `app/tracking_sync.py`
- Readers:
  - `app/add_test_tracking.py`
  - `app/fulfillment_status_report.py`
  - `app/push_tracking_to_channels.py`
  - `app/tracking_sync.py`

### `app/logs/fulfillment_status_report.json`
- Writers:
  - `app/fulfillment_status_report.py`
- Readers:
  - `app/fulfillment_status_report.py`

## Target business data flow

1. `exploration_v2.json`
   - created by product discovery
   - consumed by priority queue builder

2. `autopilot_priority_queue.json`
   - created by priority queue
   - consumed by publish execution plan

3. `publish_execution_plan.json`
   - created by publish planner
   - consumed by content, actions, listing publishers

4. `imported_skus.json`
   - registry of published/imported products
   - should contain supplier cost, shipping cost, mapping IDs, channel listing IDs

5. `*_orders.json`
   - marketplace-specific paid orders

6. `incoming_orders.json`
   - normalized paid orders from all marketplaces

7. `supplier_purchase_queue.json`
   - orders approved for supplier purchase after payment and profit recheck

8. `cj_order_drafts.json`
   - CJ draft orders

9. `cj_order_payloads.json`
   - CJ API-ready payloads

10. `cj_purchase_attempts.json`
   - purchase attempts, DRY_RUN or live

11. `tracking_updates.json`
   - tracking numbers waiting to be pushed back to marketplaces