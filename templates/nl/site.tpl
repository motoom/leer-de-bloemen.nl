<!DOCTYPE html>
<html lang="{=language}">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Leer de bloemen</title>
	<meta content="Test je kennis van bloemen, door te raden welke naam bij een foto van een bloem hoort. Hierdoor leer je makkelijk bloemen in je omgeving te herkennen." name="description" />
	<meta content="bloemen,raden,bloemen raden,bloemen quiz,bloemen leren,bloemenpracht,spel,quiz" name="keywords" />
	<meta name="google-site-verification" content="OO2IbL6bpY31noOqo8D4UPG-RB_N3h5usvcjhwCR9lU" />
	<link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico" />
	<link rel="stylesheet" type="text/css" href="/css/reset.css" />
	<link rel="stylesheet" type="text/css" href="/css/site.css" />
	<link rel="stylesheet" type="text/css" href="/css/bubble.css" />
</head>
<body>
<div id="content">
	{?answers
	<h1>Welke bloem is dit?</h1>
	<p><ul class="mchoice">
		{#answers
		<li><a href="{=url}">{=answer}</a></li>
		}
	</ul></p>
	<br clear="all" />
	<p>
	    <img class="shadow rounded" src="{=prompt}" alt="Welke bloem is dit?">
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
		<li><a href="showall">Bekijk alle bloemen</a></li>
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
	<a href="http://twitter.com/share?original_referer=&text=Leer%20de%20bloemen&url=http%3A%2F%2Fwww.leer-de-bloemen.nl" title="Tweet deze site naar je vrienden en vriendinnen!"><img align="right" src="img/twitter.gif"></a>
</div>

<div id="grond">
<p class="bronvermelding">
{?attribution Foto van bloem: {=attribution}, {=license}.<br />}
Vormgeving en webprogrammering door <a target="_new" href="http://www.michielovertoom.com">Michiel Overtoom</a>.<br />
Jouw <a href="mailto:motoom@xs4all.nl">mening</a> over deze site stel ik zeer op prijs.
<!-- Lees de <a target="_new" href="privacyverklaring">Privacy-verklaring</a> -->
</p>
</div>

</body>
</html>
