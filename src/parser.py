import re


def get_content_of_parameter(regex, commit):
    matches = re.finditer(regex, commit, re.MULTILINE)
    matched_parameters = []
    for match in matches:
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            matched_parameters.append(match.group(groupNum))
    return matched_parameters


def get_environment_parameter_operation(commit, type="added"):
    """
    this function will look for which environment parameters added or changed in the given
    commit message
    :param commit:
    :param type:
    :return:
    """
    regex = r"--env-added=(.*?)--" if type == "added" else r"--env-changed=(.*?)--"
    return get_content_of_parameter(regex, commit)


def get_commands_to_execute(commit):
    """
    this function will try to match any commmands to execute in given commit message
    :param commit:
    :return:
    """
    regex= r"--execute-command=(.*?)--"
    return get_content_of_parameter(regex,commit)


def try_to_get_type_and_group_from_commit(commit):
    regex = r"(.*?)\((.*)\):"
    matches = re.finditer(regex, commit, re.MULTILINE)
    ready_to_return = []
    for matchNum,match in enumerate(matches):
        if matchNum == 0 and match.pos != 0:
            return None
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            value = match.group(groupNum)
            ready_to_return.append(value)
    groups = ready_to_return[1].split(',') if len(ready_to_return) > 1 else ["other"]
    return None if len(ready_to_return) == 0 else {
        "type": str(ready_to_return[0]).strip(),
        "group": list(map(lambda  x: str(x).strip(), groups))
    }

def add_author_to_commands_and_environments(commands, metadata):
    return list(
        map(
            lambda x: x+" by " + metadata['author'],
            commands
        )
    )


def get_all_changelist(commits):
    changelog = []
    for commit in commits:
        commit_text = commit['message'] + ' ' + commit['title']
        changelog.append(parse_commit(commit_text, metadata=commit))
    return changelog

def parse_commit(commit, metadata):
    """
        this function will parse given commit and get the results
    """
    execute_commands = get_commands_to_execute(commit)
    added_environments = get_environment_parameter_operation(commit)
    changed_environments = get_environment_parameter_operation(commit, type="changed")
    type_and_group = try_to_get_type_and_group_from_commit(commit)
    metadata['commit'] = metadata['title'] + ' ' + metadata['message']
    response =  {
        "execute_commands":  execute_commands,
        "added_environments": added_environments,
        "changed_environments": changed_environments,
        "metadata": metadata
    }

    if type_and_group is not None and  type_and_group['type'] is not None and type_and_group['group'] is not None:
        response = {**response, **type_and_group}

    return response