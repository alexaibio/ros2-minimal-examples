from setuptools import find_packages, setup

package_name = 'turtle_ctrl_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),

    # Tell the installer which non-Python files should be installed and where.
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/turtle.launch.py']),
        ('share/' + package_name, ['launch/turtle_ctrl.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosuser',
    maintainer_email='github.alex.ai@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
