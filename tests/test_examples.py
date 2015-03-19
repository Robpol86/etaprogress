import os
import subprocess
import sys


def test_example_progress_bar():
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    cmd = [sys.executable, path, 'progress_bar', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_progress_bar_bits():
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    cmd = [sys.executable, path, 'progress_bar_bits', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_progress_bar_bytes():
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    cmd = [sys.executable, path, 'progress_bar_bytes', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_progress_bar_wget():
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    cmd = [sys.executable, path, 'progress_bar_wget', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_progress_bar_yum():
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    cmd = [sys.executable, path, 'progress_bar_yum', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_colors():
    path = os.path.join(os.path.dirname(__file__), '..', 'example_colors.py')
    cmd = [sys.executable, path, 'run', '-f']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_example_wget():
    path = os.path.join(os.path.dirname(__file__), '..', 'example_wget.py')
    cmd = [sys.executable, path, '--help']
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
