# Base image: Ruby with necessary dependencies for Jekyll
FROM ruby:3.2

# 安装系统依赖（完整补齐 Jekyll 需要的包）
RUN apt-get update && apt-get install -y \
    build-essential \
    nodejs \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户（与 devcontainer.json 一致）
RUN groupadd -g 1000 vscode && \
    useradd -m -u 1000 -g vscode vscode

# 工作目录
WORKDIR /usr/src/app

# 赋予权限
RUN chown -R vscode:vscode /usr/src/app

# 切换普通用户
USER vscode

# 复制 Gemfile
COPY Gemfile ./

# 安装 bundler（使用项目兼容版本）
RUN gem install bundler -v 2.3.26

# 安装 Jekyll 所有依赖
RUN bundle install

# 启动命令（与 docker-compose.yml 保持一致）
CMD ["bundle", "exec", "jekyll", "serve", "-H", "0.0.0.0", "-w", "--config", "_config.yml,_config_docker.yml"]
