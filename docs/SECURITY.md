# Security Guidelines - Kongtze Project

## ⚠️ CRITICAL: Never Commit Secrets to Git

### What NOT to Commit

**NEVER commit these to version control:**
- API keys (Gemini, OpenAI, etc.)
- Database passwords
- JWT secret keys
- OAuth client secrets
- Private keys or certificates
- Access tokens
- Any credentials or passwords

### ✅ Proper Credential Management

#### 1. Use Environment Variables

**Backend (.env file)**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/kongtze

# Security
JWT_SECRET_KEY=your-secure-random-secret-key-here
BCRYPT_SALT_ROUNDS=12

# AI Services
GEMINI_API_KEY=your_gemini_api_key_here

# CORS
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local file)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 2. .gitignore Configuration

Ensure your `.gitignore` includes:
```
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Credentials
*.pem
*.key
*.crt
credentials.json
secrets.json
```

#### 3. Example Environment Files

Create `.env.example` files (safe to commit) with placeholder values:

**Backend (.env.example)**
```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/kongtze
JWT_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your_gemini_api_key_here
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local.example)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 🔍 How to Check for Exposed Secrets

#### Before Committing
```bash
# Search for potential API keys
grep -r "AIzaSy" . --exclude-dir={node_modules,venv,.git}

# Search for database passwords
grep -r "postgres:postgres" . --exclude-dir={node_modules,venv,.git}

# Search for JWT secrets
grep -r "JWT_SECRET" . --exclude-dir={node_modules,venv,.git}
```

#### Check Git History
```bash
# Search commit history for secrets
git log -p | grep -i "api_key\|password\|secret"

# Check what's staged
git diff --cached
```

### 🚨 If You Accidentally Committed Secrets

#### 1. Immediate Actions
1. **Revoke the exposed credentials immediately**
   - Regenerate API keys
   - Change passwords
   - Rotate JWT secrets

2. **Remove from Git history**
```bash
# For the most recent commit
git reset HEAD~1
git add .
git commit -m "Remove exposed credentials"

# For older commits (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all
```

3. **Force push (if already pushed)**
```bash
git push origin --force --all
```

⚠️ **Warning**: Force pushing rewrites history. Coordinate with team members.

### 🔐 Production Security Checklist

#### Environment Variables
- [ ] All secrets stored in environment variables
- [ ] No hardcoded credentials in code
- [ ] `.env` files in `.gitignore`
- [ ] `.env.example` files created with placeholders

#### Database Security
- [ ] Strong database passwords (16+ characters)
- [ ] Database user has minimal required permissions
- [ ] Database not exposed to public internet
- [ ] SSL/TLS enabled for database connections

#### API Security
- [ ] JWT secrets are cryptographically random (32+ bytes)
- [ ] API keys rotated regularly
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Input validation on all endpoints

#### File Security
- [ ] Uploaded files validated (type, size)
- [ ] Files stored outside web root
- [ ] File permissions properly set
- [ ] No directory listing enabled

### 🛡️ Security Best Practices

#### 1. Generate Strong Secrets
```bash
# Generate random JWT secret (Python)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate random JWT secret (OpenSSL)
openssl rand -base64 32
```

#### 2. Use Secret Management Services

**For Production:**
- AWS Secrets Manager
- Google Cloud Secret Manager
- Azure Key Vault
- HashiCorp Vault
- Railway/Vercel environment variables

#### 3. Principle of Least Privilege
- Database users should have minimal permissions
- API keys should have minimal scopes
- Service accounts should have minimal roles

#### 4. Regular Security Audits
```bash
# Check for exposed secrets in dependencies
npm audit

# Check Python dependencies
pip-audit

# Scan for secrets in codebase
git secrets --scan
```

### 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)
- [12-Factor App: Config](https://12factor.net/config)

### 🔄 Credential Rotation Schedule

| Credential Type | Rotation Frequency |
|----------------|-------------------|
| API Keys | Every 90 days |
| Database Passwords | Every 90 days |
| JWT Secrets | Every 180 days |
| OAuth Secrets | Every 180 days |

### 📞 Security Incident Response

If you discover a security issue:
1. **Do not** commit the fix to public repository
2. Revoke compromised credentials immediately
3. Assess the impact (who had access, for how long)
4. Document the incident
5. Implement preventive measures

---

## Current Status

✅ **Fixed Issues:**
- Removed exposed Gemini API key from `kongtze-frontend/IMPLEMENTATION_SUMMARY.md`
- Removed exposed database password from documentation
- Verified `.env` files are not tracked by git
- Confirmed `.gitignore` properly excludes sensitive files

⚠️ **Action Required:**
1. Regenerate the exposed Gemini API key at https://makersuite.google.com/app/apikey
2. Update the new key in your local `.env` file
3. Never commit the actual `.env` file to git

---

**Last Updated**: 2026-01-28  
**Reviewed By**: Claude Sonnet 4.5
