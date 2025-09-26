# Tailspin Toys

This repository contains the project for a 1 hour guided workshop to explore GitHub Copilot Agent Mode and related features in Visual Studio Code. The project is a website for a fictional game crowd-funding company, with a [Flask](https://flask.palletsprojects.com/en/stable/) backend using [SQLAlchemy](https://www.sqlalchemy.org/) and [Astro](https://astro.build/) frontend using [Svelte](https://svelte.dev/) for dynamic pages.

To begin the workshop, start at [docs/README.md](./docs/README.md)

Or, if just want to run the app...

## Launch the site

A script file has been created to launch the site. You can run it by:

```bash
./scripts/start-app.sh
```

Then navigate to the [website](http://localhost:4321) to see the site!

## Additional Projects

### Sudoku Game

A separate, standalone Sudoku game has been added to the repository in the `sudoku-game/` directory. This is a complete web-based Sudoku game with:

- 🎯 Multiple difficulty levels (Easy, Medium, Hard)
- 🔍 Smart hint system
- ⏱️ Timer functionality  
- 💡 Input validation and error highlighting
- 🎨 Beautiful responsive design with dark theme
- 🎮 Complete game controls (new game, reset, clear)

To run the Sudoku game:

```bash
cd sudoku-game
pip install -r requirements.txt
python app.py
```

Then navigate to [http://localhost:5001](http://localhost:5001) to play!

See the [Sudoku Game README](./sudoku-game/README.md) for more details.

## License 

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) for the full terms.

## Maintainers 

You can find the list of maintainers in [CODEOWNERS](./.github/CODEOWNERS).

## Support

This project is provided as-is, and may be updated over time. If you have questions, please open an issue.
