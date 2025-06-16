import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from aider.io import InputOutput
    from aider.models import Model
    from aider.repo import GitRepo
    from aider.repomap import RepoMap
except ImportError:
    print(
        "Erreur : Assurez-vous que 'aider-chat' est installé (`pip install aider-chat`).",
        file=sys.stderr,
    )
    sys.exit(1)


def main():
    """
    Génère et affiche la carte du référentiel pour le projet git actuel.
    """
    io = InputOutput()

    try:
        # Initialise GitRepo pour trouver la racine du dépôt et les fichiers suivis
        repo = GitRepo(io, fnames=[], git_dname=None)
        all_files_rel = repo.get_tracked_files()
        all_files_abs = [os.path.join(repo.root, f) for f in all_files_rel]
    except FileNotFoundError:
        print(
            "Erreur : Aucun dépôt git n'a été trouvé dans le répertoire actuel.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de l'initialisation du dépôt git : {e}", file=sys.stderr)
        sys.exit(1)

    # Utilise un modèle par défaut pour le comptage des jetons (ne fait pas d'appels API)
    model = Model("gpt-4o-mini")

    # Initialise RepoMap avec une limite de jetons généreuse pour obtenir une carte complète
    repo_map_generator = RepoMap(
        root=repo.root,
        map_tokens=8192,
        main_model=model,
        io=io,
        verbose=False,
    )

    print("Génération de la carte du référentiel...", file=sys.stderr)

    # Génère la carte pour tous les fichiers du dépôt
    map_content = repo_map_generator.get_repo_map(
        chat_files=[], other_files=all_files_abs, force_refresh=True
    )
                                                                                                                                                                                                                                          
    if map_content:
        # Affiche le contenu de la carte sur la sortie standard
        print(map_content)
    else:
        print("Impossible de générer la carte du référentiel.", file=sys.stderr)


if __name__ == "__main__":
    main()