import argparse
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description='doccano.')
    parser.add_argument('--username', type=str, default='admin', help='admin username')
    parser.add_argument('--password', type=str, default='password', help='admin password')
    parser.add_argument('--email', type=str, default='example@example.com', help='admin email')
    parser.add_argument('--port', type=int, default=8000, help='port')
    parser.add_argument('--workers', type=int, default=1, help='workers')
    parser.add_argument('--database_url', type=str, default='sqlite:///doccano.db', help='data store')
    args = parser.parse_args()

    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('DATABASE_URL', args.database_url)

    print('Setup Database.')
    base = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    manage_path = os.path.join(base, 'manage.py')
    subprocess.call(['python', manage_path, 'wait_for_db'], shell=False)
    subprocess.call(['python', manage_path, 'migrate'], shell=False)
    subprocess.call(['python', manage_path, 'create_roles'], shell=False)

    print('Create admin user.')
    subprocess.call(['python', manage_path, 'create_admin',
                     '--username', args.username,
                     '--password', args.password,
                     '--email', args.email,
                     '--noinput'], shell=False)

    print(f'Starting server with port {args.port}.')
    subprocess.call(['python', manage_path, 'runserver', f'0.0.0.0:{args.port}'])


if __name__ == '__main__':
    main()
