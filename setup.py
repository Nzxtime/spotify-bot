import setuptools

setuptools.setup(
    name="spotify-bot",
    version="1.0.7",
    author="Nzxtime",
    author_email="marcel.streicher58@gmail.com",
    description="A twitch bot which can control your spotify account",
    long_description="A twitch bot which can control your spotify account. It can queue songs to a specific playlist, skip songs on request, return your current song and many more.",
    long_description_content_type="text/markdown",
    url="https://github.com/Nzxtime/spotify-bot",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['spotify-bot=spotify_bot.bot:main']},
    install_requires=['spotipy', 'twitchio'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
