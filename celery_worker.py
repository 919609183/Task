from app import app
from app.tasks import celery

if __name__ == '__main__':
    with app.app_context():
        celery.worker_main(['-A', 'celery_worker.celery', 'worker', '--loglevel=info'])
