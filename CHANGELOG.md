# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added

- Dockerfile for building and publishing the backend service image in CI/CD.

### Changed

- GitLab CI now publishes backend images to the GitLab container registry.
- updated version for python multipart
- fixed the deployment failure exit code from 0 to 1

## [0.1.0] - 2026-08-26

### Added

- FastAPI portfolio APIs for auth, projects, blog posts, certifications, uploads, and health checks.
- SQLAlchemy models, Alembic migrations, and MinIO-compatible asset storage support.
- GitHub Actions and GitLab CI/CD templates for linting, testing, auditing, packaging, and optional deployment.
- Repository release metadata via `VERSION` and this changelog.

### Changed

- Updated API route and dependency execution to the async path used by the current FastAPI test stack.
- Moved API tests to `httpx.AsyncClient` with ASGI transport for stable automated checks.
