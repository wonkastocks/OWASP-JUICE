# IMPORTANT: SSH Password Configuration

## The actual password is: $$R00tbeer02

## How to use it in different contexts:

### In Expect scripts (.exp files):
```bash
set password {\$\$R00tbeer02}
# OR
send "\$\$R00tbeer02\r"
```

### In Node.js/JavaScript:
```javascript
password: '$$R00tbeer02'  // No escaping needed in JS strings
```

### In Shell/Bash:
```bash
sshpass -p '\$\$R00tbeer02' ssh root@155.138.197.128
```

### REMEMBER:
- The password starts with TWO dollar signs: $$
- In Expect scripts, escape each $ with backslash: \$\$
- In JavaScript strings, no escaping needed
- Always test the password format if SSH fails!
```