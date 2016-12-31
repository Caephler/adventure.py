#!python3

import adventure as adv
import story


def main():
    term = adv.Terminal()
    term.use_story(story.Story())
    term.start_story()

if __name__ == "__main__":
    main()
