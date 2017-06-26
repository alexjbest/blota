import os
from django.core.management.base import BaseCommand, CommandError
from xml.dom import minidom
from question.models import Question, File

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Parses the xml files to create questions.'

    def handle(self, *args, **options):
        def getText(nodelist):
            rc = []
            for node in nodelist:
                if (node.nodeType == node.TEXT_NODE):
                    rc.append(unicode(node.nodeValue))
                elif (node.nodeName == "m"):
                    rc.append("\(" + getText(node.childNodes) + "\)")
                elif (node.nodeName == "me") or (node.nodeName == "men"):
                    rc.append("\[" + getText(node.childNodes) + "\]")
                elif (node.nodeName == "md"):
                    rc.append("\\begin{align*}" + getText(node.childNodes) + "\\end{align*}")
                elif (node.nodeName == "mrow"):
                    rc.append(getText(node.childNodes) + "\\\\")
                elif (node.nodeName == "ol"):
                    rc.append("<ol>" + getText(node.childNodes) + "</ol>")
                elif (node.nodeName == "ul"):
                    rc.append("<ul>" + getText(node.childNodes) + "</ul>")
                elif (node.nodeName == "li"):
                    rc.append("<li>" + getText(node.childNodes) + "</li>")
                elif (node.nodeName == "xref"):
                    if (node.childNodes):
                        rc.append(getText(node.childNodes))
                    else:
                        rc.append(str(node.attributes["ref"].value))
                else: # <term>, etc.
                    rc.append(getText(node.childNodes))
            return ''.join(rc)

        # Delete all questions
        Question.objects.filter().delete()
        File.objects.filter().delete()
        for filename in args:
            xmldoc = minidom.parse(filename)
            this_file = File(name = os.path.splitext(os.path.basename(filename))[0],
                    preamble = getText(xmldoc.getElementsByTagName('macros')[0].childNodes)) # TODO: maybe use the xml:id instead?
            this_file.save()
            # Definitions
            defns = xmldoc.getElementsByTagName('definition')
            for defn in defns:
                if (len(defn.getElementsByTagName("title")) > 0):
                    ques = Question(question = getText(defn.getElementsByTagName("title")[0].childNodes),
                            answer = getText(defn.getElementsByTagName("statement")[0].childNodes),
                            times_tried = 1,
                            times_right = 0,
                            q_type = Question.DEFN,
                            file = this_file,)
                    ques.save()
                else:
                    self.stdout.write("Definition with no title %s\n" % getText(defn.getElementsByTagName("statement")[0].childNodes))
            
            # Statements of thms, lemmas etc.
            # Proofs of thms lemmas etc. that have them
            thms = xmldoc.getElementsByTagName('theorem')
            lems = xmldoc.getElementsByTagName('lemma')
            props = xmldoc.getElementsByTagName('proposition')
            for prop in thms + lems + props:
                title = u""
                if (len(prop.getElementsByTagName("title")) > 0):
                    title = getText(prop.getElementsByTagName("title")[0].childNodes)
                    ques = Question(question = title,
                            answer = getText(prop.getElementsByTagName("statement")[0].childNodes),
                            times_tried = 1,
                            times_right = 0,
                            q_type = Question.STATE,
                            file = this_file,)
                    ques.save()
                else:
                    self.stdout.write("Proposition with no title %s\n" % getText(prop.getElementsByTagName("statement")[0].childNodes))
                if (len(prop.getElementsByTagName("proof")) > 0):
                    statement = getText(prop.getElementsByTagName("statement")[0].childNodes)
                    if title:
                        statement = title + u": " + statement
                    ques = Question(question = statement,
                            answer = getText(prop.getElementsByTagName("proof")[0].childNodes),
                            times_tried = 1,
                            times_right = 0,
                            q_type = Question.PROVE,
                            file = this_file,)
                    ques.save()
                else:
                    self.stdout.write("Proposition with no proof %s\n" % getText(prop.getElementsByTagName("statement")[0].childNodes))
            
            self.stdout.write('Successfully added questions for "%s"\n\n' % filename)
