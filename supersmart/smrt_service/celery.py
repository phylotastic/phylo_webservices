from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('smrt_service',
             broker='amqp://supersmart:supersmart@localhost:5672/supersmartvhost',
             backend='amqp://supersmart:supersmart@localhost:5672/supersmartvhost',
             include=['smrt_service.tasks'])

# Optional configuration, see the application user guide.
#app.conf.update(
#    result_expires=3600,
#)

if __name__ == '__main__':
    app.start()

