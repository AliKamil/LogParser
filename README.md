# LogParser
TestCase for Yandex
Example usage
tail -f /var/log/service.log | json-log --format template.j2 --filter @fields.level=ERROR
