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

data "yandex_function" "bot" {
  name = "awesome-bot"
}

resource "yandex_function_trigger" "timer" {
  name        = "born-be-random"
  description = "Imitate function random invocation"
  timer {
    cron_expression = "0 7-15/2 ? * * *"
  }
  function {
    id = data.yandex_function.bot.id
  }
}
