import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'cbr1_data_pipeline'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='limsengtong',
    maintainer_email='sengtonglim@gmail.com',
    description='Research data pipeline: rosbag2 recording with reproducibility metadata + CSV export.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bag_to_csv = cbr1_data_pipeline.bag_analysis:main',
        ],
    },
)
