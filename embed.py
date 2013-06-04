import os

fileTemplate = """package
{
    public class Embedded
    {%s
    }
}
"""


embedTemplate = """
        [Embed(source = '%s', mimeType='application/octet-stream')]
        private static var _%s:Class;"""

embeds = ""
names = []
for r,n,f in os.walk("."):
    for fn in f:
        ext = fn[-3:].lower()
        if not ext in [".sc", ".c8"]:
            continue
        fn = os.path.join(r,fn)

        name = fn.split("/")[-1].replace("-","").replace(".","_")
        embeds += embedTemplate % (fn,name)
        names += [name]

embeds += """

        public static var Internal:Object =
        {
"""
for n in names:
    embeds += "        '%s': new _%s(),\n" % (n.replace("_"," "),n)
embeds = embeds[:-2] + """
        }"""

fo = file("Embedded.as","w")
fo.write( fileTemplate % embeds )
fo.close()
