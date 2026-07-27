FROM python:3.11-slim

LABEL "name"="repo2prompt"
LABEL "description"="Pack any repository into clean, AI-friendly context"
LABEL "homepage"="https://github.com/wshuainanhai/repo2prompt"
LABEL "license"="MIT"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
