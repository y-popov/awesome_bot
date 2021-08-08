terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  backend "s3" {
    endpoint                    = "storage.yandexcloud.net"
    bucket                      = "mad-bucket"
    key                         = "awesome-bot.tfstate"
    region                      = "ru-central1-a"
    skip_region_validation      = true
    skip_credentials_validation = true
  }
}

provider "yandex" {
  zone = "ru-central1-a"
}

data "yandex_function_trigger" "timer" {
  trigger_id = "a1siuespk6gqpg832no6"
}
