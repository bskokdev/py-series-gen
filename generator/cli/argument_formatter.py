from argparse import HelpFormatter


class TargetHelpFormatter(HelpFormatter):
    def _format_action_invocation(self, action):
        if action.option_strings:
            return ", ".join(action.option_strings)
        return self._metavar_formatter(action, action.dest)(1)[0]
