# Production Checklist

## Before live mode

- [ ] Dashboard opens
- [ ] /production/health returns ok
- [ ] /production/config-check reviewed
- [ ] /production/safety-check reviewed
- [ ] PostgreSQL running
- [ ] DATABASE_URL correct
- [ ] Shopify token added
- [ ] Supplier API key added
- [ ] Shipping API key added
- [ ] DRY_RUN=true tested
- [ ] Shopify draft product tested
- [ ] No real purchases in dry-run
- [ ] Daily budget set
- [ ] Emergency stop tested
- [ ] Refund policy ready
- [ ] Platform rules checked
- [ ] Logs visible
- [ ] Backup strategy ready

## Live mode minimum

```env
APP_ENV=production
DRY_RUN=false
AUTONOMY_ENABLED=false
EMERGENCY_STOP=false
```

Start with AUTONOMY_ENABLED=false and create only draft listings first.
