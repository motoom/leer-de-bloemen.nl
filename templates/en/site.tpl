<!DOCTYPE html>
<html lang="{=language}">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Learn the flowers</title>
	<meta content="Test your knowledge of flowers, by guessing which name belongs to a picture of a flower. You'll learn to recognize flowers in your environment." name="description" />
	<meta content="flowers,guessing,guessing flowers,flower quiz,learning flowers,recognizing flowers,game,quiz" name="keywords" />
	<meta name="google-site-verification" content="OO2IbL6bpY31noOqo8D4UPG-RB_N3h5usvcjhwCR9lU" />
	<link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico" />
	<link rel="stylesheet" type="text/css" href="/css/reset.css" />
	<link rel="stylesheet" type="text/css" href="/css/site.css" />
	<link rel="stylesheet" type="text/css" href="/css/bubble.css" />
</head>
<body>
<div id="content">
	{?answers
	<h1>Which flower is this?</h1>
	<p><ul class="mchoice">
		{#answers
		<li><a href="{=url}">{=answer}</a></li>
		}
	</ul></p>
	<br clear="all" />
	<p>
	    <img class="shadow rounded" src="{=prompt}" alt="Which flower is this?">
	</p>
	<p class="extrawit">{=weetje}</p>
	}
	{?verdict
		{=verdict}
	}
</div>

<div id="nav">
	<ul class="nav">
		<li><a href="/">Quiz</a></li>
		<li><a href="showall">List the flowers</a></li>
	</ul>
	{?feedback
	<div class="feedback example-obtuse">
		{?progress
			<div class="progress">{=progress}</div><br />
		}
		<div class="message">{=message}</div>
	</div>
	<p><img src="{=feedbackpicture}"></p>
	}
</div>

<div id="lucht">
</div>

<div id="twitter">
	<a href="http://twitter.com/share?original_referer=&text=Learn%20the%20flowers&url=http%3A%2F%2Fwww.learn-the-flowers.com" title="Tweet this site to your friends!"><img align="right" src="img/twitter.gif"></a>
</div>

<div id="grond">
<p class="bronvermelding">
{?attribution Picture of flower: {=attribution}, {=license}.<br />}
Design and webprogramming by <a target="_new" href="http://www.michielovertoom.com">Michiel Overtoom</a>.<br />
I appreciate your <a href="mailto:motoom@xs4all.nl">feedback</a> on this site.
<!-- Read the <a target="_new" href="privacyverklaring">Privacy statement</a> -->
</p>
</div>

</body>
</html>
