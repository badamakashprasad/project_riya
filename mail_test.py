import smtplib

sender = 'akashb97@gmail.com'
receiver = 'bakashp1997@gmail.com'

msg = "\r\n".join([
  "From: user_me@gmail.com",
  "To: user_you@gmail.com",
  "Subject: Just a message",
  "",
  "Why, oh why"
  ])

username = 'akashb97@gmail.com'
password = 'akashisgreat'

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(sender,receiver,msg)
server.quit()