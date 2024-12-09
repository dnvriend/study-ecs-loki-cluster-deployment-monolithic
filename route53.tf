resource "aws_route53_zone" "services" {
  name          = "services.vpc"
  force_destroy = true

  vpc {
    vpc_id = aws_vpc.vpc.id
  }
}

resource "aws_route53_record" "loki" {
  zone_id = aws_route53_zone.services.zone_id
  name    = "loki.services.vpc"
  type    = "A"
  ttl     = "5"
  records = ["127.0.0.1"]

  lifecycle {
    ignore_changes = [records, ttl]
  }
}

resource "aws_route53_record" "grafana" {
  zone_id = aws_route53_zone.services.zone_id
  name    = "grafana.services.vpc"
  type    = "A"
  ttl     = "5"
  records = ["127.0.0.1"]
}

resource "aws_route53_record" "httpbin" {
  zone_id = aws_route53_zone.services.zone_id
  name    = "httpbin.services.vpc"
  type    = "A"
  ttl     = "5"
  records = ["127.0.0.1"]
}

