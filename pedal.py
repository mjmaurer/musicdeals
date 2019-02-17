import praw
import re
import smtplib
import constants


def main():
    reddit = praw.Reddit(user_agent='Pedals (by /u/mauflows)',
                         client_id=constants.PEDALS_ID,
                         client_secret=constants.PEDALS_SECRET)

    subreddit = reddit.subreddit('PedalDeals+SynthDeals')
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    rating = int(re.search('\\d+%$', submission.title).group(0).strip('%'))
    if (rating > 97):
        sendText(submission)


def sendText(submission):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(constants.GMAIL_USER, constants.GMAIL_PASS)
        server.sendmail(constants.GMAIL_USER, constants.GMAIL_TARGET,
                        submission.title + ' \n ' + submission.url)
    except Exception as e:
        print('Error occurred: ' + str(e))


if __name__ == '__main__':
    main()
