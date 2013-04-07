
# itembankdb.py - Software by Michiel Overtoom, motoom@xs4all.nl


easy = (
    ('0047.jpg', 'a ', 'Nettle', 'Ouch! This plant stings! Better not touch it!', 'Frank Vincentz', 'cc'),
    ('0004.jpg', 'a ', 'Buttercup', 'This flower is poisonous when eaten fresh by cattle, but their acrid taste means they are usually left uneaten.', 'Kurt Stueber', 'cc'),
    ('0066.jpg', 'a ', 'Thistle', 'Ouch! This is a prickly plant!', 'Kurt Stueber', 'cc'),
    ('0055.jpg', 'a ', 'Poppy', 'When you pick this flower, it quickly wilts.', 'Rob Hooft', 'cc'),
    ('0020.jpg', 'a ', 'Daisy', 'This flower grows everywhere in lawns.', 'Tom.k', 'cc'),
    ('0018.jpg', 'a ', 'Daffodil', 'This flower is perceived in the West as a symbol of vanity, in the East as a symbol of wealth and good fortune.', 'Martin Hirtreiter', 'cc'),
    ('0021.jpg', 'a ', 'Dandelion', 'The leaves of this flower are eaten in salads, and its roots can be used to make \'coffee\'.', 'Sebastian Stabinger/Paethon', 'cc'),
    ('0061.jpg', 'a ', 'Snowdrop', 'This plant flowers very early in the spring.', 'Caroig', 'cc'),
    ('0068.jpg', 'a ', 'Tulip', 'This flower is cultivated in a variety of colors. The Netherlands is one of the biggest exporters of this flower.', 'Robert F. Carter/Bettycrocker', 'cc'),
    ('0070.jpg', '', 'White clover', 'If this plant has four leaves, it is said to bring luck.', 'Leo Michels', 'pd'),
    ('0064.jpg', 'a ', 'Sunflower', 'This flower is grown for its seeds, which are pressed for oil, or are used in salads and breads.', 'Peter Heeling', 'pd'),
)

medium = (
    ('0024.jpg', 'a ', 'Field pansy', 'This flower is seen as a weed of disturbed and cultivated areas.', 'Peter Heeling', 'pd'),
    ('0008.jpg', '', 'Chives', 'This plant is family of the onions, leek and garlic, and is often used in salads and to flavor butter.', 'Patrick Reijnders', 'cc'),
    ('0003.jpg', '', 'Broom', 'This ornamental plant is used for sand dune stabilising.', 'MPF Newcastle', 'cc'),
    ('0019.jpg', 'a ', 'Dahlia', 'This flower comes in a variety of stunning and bright colours.', 'KayEss', 'cc'),
    ('0023.jpg', '', 'Dill', 'This plant is an herb which is often used to flavor fish and pickles.', 'Toubib', 'cc'),
    ('0022.jpg', 'a ', 'Deadnettle', 'This plant looks as if it stings, but it doesn\'t.', 'TeunSpaans', 'cc'),
    ('0011.jpg', '', 'Common hogweed', 'This plant shouldn\'t be touched, because that can lead to skin irritation.', 'Christian Fischer', 'cc'),
    ('0031.jpg', 'a ', 'Greater plantain', 'This plant is abundant beside paths, roadsides, and other areas with frequent soil compaction.', 'Rasbak', 'cc'),
    ('0038.jpg', 'an ', 'Hyacinth', 'This nicely smelling flower originated from Syria and Irak, and became popular in Europe in the 16th century.', 'Rasbak', 'cc'),
    ('0006.jpg', '', 'Chamomile', 'These flowers are used to make tea.', 'Penarc', 'cc'),
    ('0036.jpg', '', 'Honeysuckle', 'This climbing plant has a strong sweet scent in the evening.', 'Rex', 'pd'),
    ('0054.jpg', 'a ', 'Poinsettia', 'This beautifully colored flower is often associated with Christmas.', 'Scott Bauer', 'pd'),
    ('0017.jpg', 'a ', 'Cucumber', 'The fruits of this plant are eaten as vegetable, in salads.', 'USDA', 'pd'),
    ('0013.jpg', 'a ', 'Cornflower', 'In the past this flower often grew as a weed in crop fields, hence its name.', 'Maximilian Buehn', 'cc'),
    ('0050.jpg', 'an ', 'Ox eye daisy', 'This flower is often used in ornamental gardens.', 'sannse', 'cc'),
    ('0044.jpg', '', 'Mimosa', 'These flowers have small leaves and many stamens.', 'Eric Hunt', 'cc'),
    ('0052.jpg', '', 'Peppermint', 'You can make tea of this plant.', 'Sten Porse', 'cc'),
    ('0027.jpg', '', 'Giant hogweed', 'Don\'t touch this plant. It can cause skin irritation.', 'GerardM', 'cc'),
    ('0058.jpg', 'a ', 'Red clover', 'This flower was used to feed cattle.', 'Rasbak', 'cc'),
    ('0060.jpg', '', 'Rosemary', 'This nicely smelling plant is used in the kitchen.', 'Jean Tosti', 'cc'),
    ('0067.jpg', '', 'Thyme', 'This herb is used in the kitchen, but also in soap.', 'Kurt Stueber', 'cc'),
    ('0005.jpg', 'a ', 'Carnation', 'Colombia is the biggest producer of this flower.', 'Darkone', 'cc'),
    ('0025.jpg', '', 'Flax', 'This plant has been cultivated for more than six thousand years, to make linen.', 'Rasbak', 'cc'),
)

hard = (
    ('0040.jpg', 'a ', 'Jerusalem artichoke', 'This plant is cultivated for its tuber, which is used as a root vegetable.', 'Paul Fenwick', 'cc'),
    ('0000.jpg', 'an ', 'Anemone', 'This flower, which exists in many colors, is family of the buttercup.', 'Rex', 'pd'),
    ('0001.jpg', 'an ', 'Aster', 'This garden plant originated in North-America.', 'TeunSpaans', 'cc'),
    ('0041.jpg', 'a ', 'Kingcup', 'This plant is native to marshes, fens, ditches and wet woodland.', 'TeunSpaans', 'cc'),
    ('0007.jpg', '', 'Chervil', 'This plant is used in the kitchen, and is used in the French herb mixture \'fines herbes\'.', 'RasBak', 'cc'),
    ('0014.jpg', '', 'Cow parsley', 'This plant is a particularly common sight by the roadside.', 'Rasbak', 'cc'),
    ('0026.jpg', 'a ', 'Freesia', 'This flower smells so nice that it is often used in soap, shampoo, candles, etc...', 'Jeantosti', 'cc'),
    ('0028.jpg', '', 'Ginger', 'The fragrant roots of this plant are used in the kitchen.', 'Aruna', 'cc'),
    ('0033.jpg', '', 'Gypsophila', 'This plant is named after the type of soil it likes to grow on.', 'KENPEI', 'cc'),
    ('0029.jpg', '', 'Golden dock', 'This plant lives on wet, supratidal, and rainbowed terrain.', 'Christian Fischer', 'cc'),
    ('0010.jpg', 'a ', 'Common butterbur', 'This plant has big leaves and grows next to water.', 'Roger Griffith', 'pd'),
    ('0057.jpg', 'a ', 'Purple loosestrife', 'This plant was used in tanneries. The juice of its roots could be used to dye wool red.', 'Radomil', 'cc'),
    ('0015.jpg', 'a ', 'Cowslip', 'This plant is seen in open fields, meadows, and coastal dunes and clifftops.', 'Rasbak', 'cc'),
    ('0030.jpg', 'a ', 'Goldenrod', 'Inventor Thomas Edison experimented with goldenrod to produce rubber.', 'Pethan', 'cc'),
    ('0034.jpg', 'an ', 'Heath violet', 'This flower is found near fens, on moist woodlands, especially on acidic soils.', 'b.gliwa', 'cc'),
    ('0037.jpg', 'an ', 'Hortensia', 'This flower is popular because of its bright colors.', 'P.J.L Laurens', 'cc'),
    ('0039.jpg', 'an ', 'Iris', 'Depictions of this flowers can be found in the egyptian pyramids.', 'Jerzy Opiola', 'cc'),
    ('0016.jpg', 'a ', 'Crown imperial', 'This plant can be used as a mole repellent.', 'Magalhaes', 'pd'),
    ('0009.jpg', '', 'Coltsfoot', 'The ancient Romans smoked these flowers in a pipe.', 'Teun Spaans', 'cc'),
    ('0043.jpg', 'a ', 'Lily of the valley', 'This plant is grown for its scented flowers. It\'s used in perfumes and cosmetics.', 'Olegivvit', 'cc'),
    ('0046.jpg', 'a ', 'Mouse ear hawkweed', 'This plant thanks is called after it\'s hairy leaves.', 'Kurt Stueber', 'cc'),
    ('0049.jpg', 'an ', 'Orchid', 'The family of this plant has some 20.000 species.', 'Roepers', 'cc'),
    ('0053.jpg', '', 'Phlox', 'These flowers are valued in the garden for their ability to attract butterflies.', 'Atilin', 'pd'),
    ('0051.jpg', 'a ', 'Peony', 'This scented flower attracts ants, and is the national symbol of China.', 'Fanghong', 'cc'),
    ('0042.jpg', 'a ', 'Larkspur', 'This poisonous plant is loved by bees and butterflies.', 'Stan Shebs', 'cc'),
    ('0002.jpg', 'a ', 'Broadleaf dock', 'This plant is easily recognizable by its very large leaves, and is considered a weed.', 'Sten Porse', 'cc'),
    ('0065.jpg', '', 'Swamp milkweed', 'This plant is one of the best attractors of the Monarch butterfly, which feeds on the flowers and lays her eggs on them.', 'Teune', 'cc'),
    ('0035.jpg', 'an ', 'Hoary plantain', 'The ancient Romans used this plant for treating wounds and toothache.', 'Sten', 'cc'),
    ('0062.jpg', '', 'St johns wort', 'This plant was used for its medicinal qualities.', 'Michael H. Lemmer', 'cc'),
    ('0048.jpg', 'an ', 'Opium poppy', 'From this plant seeds are extracted, which are used on breads and donuts.', 'Louise Joly', 'cc'),
    ('0059.jpg', 'a ', 'Ribwort plantain', 'This plant is a common weed of cultivated land.', 'Hans Hillewaert', 'cc'),
    ('0056.jpg', 'a ', 'Primrose', 'The flowers of this plant are sometimes used to make tea and to flavour wine.', 'Teun Spaans', 'cc'),
    ('0069.jpg', '', 'Valerian', 'This flower attracts cats, which find its scent irrisitible.', 'Pethan', 'cc'),
    ('0063.jpg', '', 'Stonecrop', 'This plant has water-storing leaves. They\'re also used on green roofs.', 'Darkone', 'cc'),
    ('0012.jpg', '', 'Common soapwort', 'The roots of this plant were used to bleach laundry.', 'Teun Spaans', 'cc'),
    ('0032.jpg', '', 'Ground elder', 'The tender leaves of this plant have been used as a spring leaf vegetable, much as spinach was used.', 'Caronna', 'cc'),
    ('0045.jpg', 'a ', 'Mountain pansy', 'This flower has adapted itself to certain mining areas.', 'Friedrich Holtz', 'cc'),
)

itembanks = (
    ("Wellknown flowers",
        easy,
        "<p>We start with some well known flowers. After you make two correct guesses at a flower, I wont't ask it again.</p><p>It's OK when you guess a flower wrong, I'll just show you the right answer.</p><p>Go ahead!</p>",
        "<p>Well done, you now know all the easy flowers. Let's proceed to the somewhat lesser known flowers!</p>",
        ),
    ("Somewhat less known flowers",
        medium,
        "<p>Now, the somewhat lesser known flowers.</p><p>Will you recognize them all?</p>",
        "<p>Hooray! There are even lesser known flowers. Are you ready for them?</p>",
        ),
    ("Hard-to-guess flowers",
        hard,
        "<p>Finally, the hard-to-guess flowers.</p><p>Let's see how quickly you can learn them!</p>",
        "<p>That was all... You now know all the flowers on this website. Great job!</p>",
        ),
    )

if __name__ == "__main__":
    import sqlite3
    # con = sqlite3.connect("/Users/user/Sites/learnthethings/things.db")
    c = con.cursor()
    c.row_factory = sqlite3.Row
    # for r in c.execute("select * from learnthethings_level"): print r["id"], r["title"]
    # id 1 Wellknown flowers
    # id 2 Somewhat less known flowers
    # id 3 Hard-to-guess flowers
    for level, itembank in ((1, easy), (2, medium), (3, hard)):
        c.execute("delete from learnthethings_item where level_id=?", (level,))
        print "Level", level
        for (image, article, name, hint, attribution, license) in itembank:
            image = image.replace(".jpg", "")
            print image, name
            c.execute("""
                insert into learnthethings_item(level_id, image, article, name, hint, attribution, license) 
                values (?,?,?,?,?,?,?)
                """, (level, image, article, name, hint, attribution, license))
    con.commit()
    