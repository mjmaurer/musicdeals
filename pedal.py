import praw
import re
import smtplib
import constants
import datetime 

def main():
    reddit = praw.Reddit(user_agent='Pedals (by /u/mauflows)',
                         client_id=constants.PEDALS_ID,
                         client_secret=constants.PEDALS_SECRET)
    startTime = datetime.datetime.now();
    subreddit = reddit.subreddit('PedalDeals+SynthDeals')
    for submission in subreddit.stream.submissions():
        process_submission(submission, startTime)


def process_submission(submission, startTime):
    try:
        rating = int(re.search('\\d+%$', submission.title).group(0).strip('%'))
        postTime = datetime.datetime.fromtimestamp(submission.created)
        if (rating > 97 and postTime > startTime):
            print('sending text')
            print('start time: ' + startTime.strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
            print('post time: ' + postTime.strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
            sendText(submission)
    except Exception as e:
        print('Bad title?: ' + str(submission.title))

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
