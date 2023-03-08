# Repo Resource
resource "github_repository" "repo" {
  name       = var.repo_name
  visibility = var.visibility
}