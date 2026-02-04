#!/bin/bash
# Enhanced zcoder skills installation script
# Run this on zcoder node to supercharge coding capabilities

set -e

echo "🚀 Setting up Enhanced Coding Skills for zcoder..."
echo "📊 Installing 15 premium coding skills from OpenClaw registry..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Check if clawhub is available
if ! command -v npx &> /dev/null; then
    error "npx not found. Please install Node.js first."
    exit 1
fi

# Create skills directory structure
SKILLS_DIR="/root/.openclaw/skills/zcoder-enhanced"
mkdir -p "$SKILLS_DIR"
log "Created skills directory: $SKILLS_DIR"

# Core development skills
CORE_SKILLS=(
    "senior-fullstack"
    "nextjs-expert"
    "vercel-react-best-practices"
    "ui-ux-master"
    "docker-essentials"
    "k8s-skills"
    "aws-solution-architect"
    "azure-infra"
    "tdd-guide"
    "debug-pro"
    "agenticflow-skill"
    "mcp-builder"
    "react-email-skills"
    "remotion-video-toolkit"
    "backend-patterns"
)

# Install skills
log "Installing ${#CORE_SKILLS[@]} premium coding skills..."

for skill in "${CORE_SKILLS[@]}"; do
    log "Installing: $skill"
    
    # Install via clawhub
    if npx clawhub@latest install "$skill" --dir="$SKILLS_DIR/$skill"; then
        log "✅ Successfully installed: $skill"
    else
        warning "⚠️  Could not install: $skill (may not exist in registry)"
    fi
done

# Create skill registry
log "Creating skill registry..."
cat > "$SKILLS_DIR/registry.json" << EOF
{
  "zcoder_enhanced_skills": {
    "version": "1.0.0",
    "installed_skills": [${CORE_SKILLS[@]/%/"&"}],
    "categories": {
      "fullstack": ["senior-fullstack", "nextjs-expert", "vercel-react-best-practices"],
      "infrastructure": ["docker-essentials", "k8s-skills", "aws-solution-architect", "azure-infra"],
      "quality": ["tdd-guide", "debug-pro"],
      "ai_integration": ["agenticflow-skill", "mcp-builder"],
      "specialized": ["react-email-skills", "remotion-video-toolkit", "backend-patterns"]
    },
    "usage_examples": {
      "create_nextjs_project": "Use senior-fullstack + nextjs-expert",
      "deploy_to_aws": "Use aws-solution-architect + docker-essentials",
      "optimize_performance": "Use vercel-react-best-practices + debug-pro",
      "create_email_system": "Use react-email-skills + backend-patterns"
    }
  }
}
EOF

# Create usage guide
cat > "$SKILLS_DIR/README.md" << EOF
# Enhanced zcoder Skills Package

## Installed Skills (${#CORE_SKILLS[@]} total)

### Full-Stack Development
- **senior-fullstack**: Complete project scaffolding (Next.js/FastAPI/MERN/Django)
- **nextjs-expert**: Next.js 14/15 with App Router expertise
- **vercel-react-best-practices**: Vercel engineering performance optimization

### Infrastructure & DevOps
- **docker-essentials**: Container management and orchestration
- **k8s-skills**: Kubernetes cluster management (autoscaling, backup, certs)
- **aws-solution-architect**: AWS serverless patterns and IaC templates
- **azure-infra**: Azure cloud management and deployment

### Quality Assurance
- **tdd-guide**: Test-driven development with coverage analysis
- **debug-pro**: Systematic debugging across languages and frameworks

### AI & Modern Development
- **agenticflow-skill**: AI workflow and agent orchestration
- **mcp-builder**: Model Context Protocol server development
- **react-email-skills**: Responsive HTML email development
- **remotion-video-toolkit**: Programmatic video creation with React
- **backend-patterns**: API design and database optimization

## Quick Usage Examples

\`\`\`bash
# Create full-stack project
zcoder.sh code "Use senior-fullstack to create Next.js + FastAPI crypto dashboard"

# Optimize React performance  
zcoder.sh code "Use vercel-react-best-practices to audit and optimize my React app"

# Deploy to AWS
zcoder.sh code "Use aws-solution-architect to create serverless crypto API architecture"

# Debug and test
zcoder.sh code "Use debug-pro and tdd-guide to fix bugs in my Node.js application"
\`\`\`

## Power Features

- **Cost**: All skills use local Qwen 32B (FREE tokens)
- **Quality**: 1700+ community-vetted skills
- **Performance**: GPU-accelerated generation
- **Coverage**: From frontend to infrastructure

## Next Steps

1. Test skills with sample projects
2. Create custom skills for your specific needs
3. Share improvements back to community

## Support

Skills installed at: $SKILLS_DIR
Registry: $SKILLS_DIR/registry.json
EOF

# Create quick start script
cat > "$SKILLS_DIR/quick_start.sh" << 'EOF'
#!/bin/bash
echo "🚀 zcoder Enhanced Skills Quick Start"
echo "Available commands:"
echo ""
echo "1. Create Next.js project:"
echo "   zcoder.sh code 'Use senior-fullstack to create Next.js crypto dashboard'"
echo ""
echo "2. Optimize React performance:"
echo "   zcoder.sh code 'Use vercel-react-best-practices to optimize my React app'"
echo ""
echo "3. Deploy with Docker:"
echo "   zcoder.sh code 'Use docker-essentials to containerize my Node.js app'"
echo ""
echo "4. Create AWS serverless API:"
echo "   zcoder.sh code 'Use aws-solution-architect to create serverless crypto API'"
echo ""
echo "5. Debug and test:"
echo "   zcoder.sh code 'Use debug-pro and tdd-guide to fix bugs in my app'"
EOF

chmod +x "$SKILLS_DIR/quick_start.sh"

# Verification
log "🔍 Verifying installation..."
INSTALLED_COUNT=$(ls -1 "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l)
log "Successfully installed $INSTALLED_COUNT enhanced coding skills"

# Create summary
log "🎉 zcoder enhancement complete!"
echo ""
echo "📋 Summary:"
echo "   Skills Directory: $SKILLS_DIR"
echo "   Registry: $SKILLS_DIR/registry.json"
echo "   Usage Guide: $SKILLS_DIR/README.md"
echo "   Quick Start: $SKILLS_DIR/quick_start.sh"
echo ""
echo "🚀 zcoder is now supercharged with premium coding skills!"
echo "💡 Use: bash $SKILLS_DIR/quick_start.sh for examples"