import typer
import json
from src.parser import parse_commit, add_author_to_commands_and_environments, get_all_changelist

app = typer.Typer()


@app.command(name="commit-list")
def get_commit_list(dir: str = '.', since: str | None = None, until: str = 'HEAD'):
    list = get_commits(dir=dir, since=since, until=until)
    typer.echo(json.dumps(list))


@app.command(name="changelog")
def get_changelog(dir: str = '.', since: str | None = None, until: str = 'HEAD'):
    commits = get_commits(dir=dir, since=since, until=until)
    changelist = get_all_changelist(commits)
    changelog = {}

    for change in changelist:
        groups =  change['group'] if 'group' in change and change['group'] is not None else ['other']
        type = change['type'] if 'type' in change and change['type'] is not None else 'unknown'
        for group in groups:
            if group not in changelog:
                changelog[group] = {}

            if type not in changelog[group]:
                changelog[group][type] = {
                    "all_commits": [],
                    "execute_commands": [],
                    "added_environments": [],
                    "changed_environments": []
                }

            changelog[group][type]['all_commits'] = [*changelog[group][type]['all_commits'], change['metadata']['title'] + change['metadata']['message']]
            changelog[group][type]['execute_commands'] = [*changelog[group][type]['execute_commands'], *change['execute_commands']]
            changelog[group][type]['added_environments'] = [*changelog[group][type]['added_environments'], *change['added_environments']]
            changelog[group][type]['changed_environments'] = [*changelog[group][type]['changed_environments'], *change['changed_environments']]


    typer.echo(json.dumps(changelog))


@app.command(name='deployment-note')
def get_deployment_note(dir: str = '.', since: str | None = None, until: str = 'HEAD'):
    commits = get_commits(dir=dir, since=since, until=until)
    changelog = get_all_changelist(commits)
    execute_commands = []
    added_environments = []
    changed_environments = []
    all_commits = []

    for change in changelog:
        execute_commands = [*execute_commands, *add_author_to_commands_and_environments(
            change['execute_commands'], change['metadata']
        )]
        added_environments = [*added_environments, *add_author_to_commands_and_environments(
            change['added_environments'], change['metadata']
        )]
        changed_environments = [*changed_environments, *add_author_to_commands_and_environments(
            change['changed_environments'], change['metadata']
        )]
        all_commits.append(
            change['metadata']['commit']
        )

    response = {
        "all_commits": all_commits,
        "execute_commands": execute_commands,
        "added_environments": added_environments,
        "changed_environments": changed_environments
    }

    typer.echo(json.dumps(response))


from src.helper import get_commits

if __name__ == '__main__':
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
