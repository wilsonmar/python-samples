pid_file = "./vault-agent.pid"

vault {
  address = "http://0.0.0.0:8200"
}

auto_auth {
  method "approle" {
    config = {
      role_id_file_path   = "role_id-webapp"
      secret_id_file_path = "secret_id-webapp"
      remove_secret_id_file_after_reading = false
    }
  }

  sink "file" {
    config = {
      path = "./agent-token"
    }
  }

}

cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address     = "0.0.0.0:8100"
  tls_disable = true
}
