from setuptools import setup

package_name = 'find_edge_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='daniel',
    maintainer_email='game48875@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'capture = find_edge_pkg.capture:main',
            'find_edge = find_edge_pkg.find_edge:main',
            'display = find_edge_pkg.display:main',
            'event = find_edge_pkg.event:main'
        ],
    },
)
