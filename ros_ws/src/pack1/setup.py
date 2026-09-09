from setuptools import find_packages, setup
from glob import glob
package_name = 'pack1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'basic_node=pack1.basic_node:main',
            'publisher=pack1.publisher:main',
            'GoToGoalNode=pack1.GoToGoalNode:main',
            'go_to_goal=pack1.go_to_goal:main',
            'go_to_goal_client=pack1.go_to_goal_client:main',
            'go_goal.launch=launch.go_goal.launch:main'

        ],
    },
)
