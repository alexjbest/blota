from django.core.management.base import BaseCommand, CommandError
from xml.dom import minidom
from question.models import Question

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Parses the xml files to create questions.'

    def handle(self, *args, **options):
        def getText(nodelist):
            rc = []
            for node in nodelist:
                if (node.nodeType == node.TEXT_NODE):
                    rc.append(str(node.nodeValue))
                elif (node.nodeName == "m"):
                    rc.append("\(" + getText(node.childNodes) + "\)")
                elif (node.nodeName == "me"):
                    rc.append("\[" + getText(node.childNodes) + "\]")
                elif (node.nodeName == "ol"):
                    rc.append("<ol>" + getText(node.childNodes) + "</ol>")
                elif (node.nodeName == "ul"):
                    rc.append("<ul>" + getText(node.childNodes) + "</ul>")
                elif (node.nodeName == "li"):
                    rc.append("<li>" + getText(node.childNodes) + "</li>")
            return ''.join(rc)
        Question.objects.filter().delete()
        for filename in args:
            xmldoc = minidom.parse(filename)
            # Definitions
            defns = xmldoc.getElementsByTagName('definition')
            for defn in defns:
                if (len(defn.getElementsByTagName("title")) > 0):
                    ques = Question(question = "Define: %s" % getText(defn.getElementsByTagName("title")[0].childNodes),
                            answer = getText(defn.getElementsByTagName("statement")[0].childNodes),
                            times_tried = 1,
                            times_right = 0)
                    ques.save()
                else:
                    self.stdout.write("Definition with no title %s\n" % getText(defn.getElementsByTagName("statement")[0].childNodes))
            
            # Statements of thms, lemmas etc.
            # Proofs of thms lemmas etc. that have them
            thms = xmldoc.getElementsByTagName('theorem')
            lems = xmldoc.getElementsByTagName('lemma')
            props = xmldoc.getElementsByTagName('proposition')
            for prop in thms + lems + props:
                if (len(prop.getElementsByTagName("title")) > 0):
                    ques = Question(question = "State: %s" % getText(prop.getElementsByTagName("title")[0].childNodes),
                            answer = getText(prop.getElementsByTagName("statement")[0].childNodes),
                            times_tried = 1,
                            times_right = 0)
                    ques.save()
                else:
                    self.stdout.write("Proposition with no title %s\n" % getText(prop.getElementsByTagName("statement")[0].childNodes))
                if (len(prop.getElementsByTagName("proof")) > 0):
                    ques = Question(question = "Prove: %s" % getText(prop.getElementsByTagName("statement")[0].childNodes),
                            answer = getText(prop.getElementsByTagName("proof")[0].childNodes),
                            times_tried = 1,
                            times_right = 0)
                    ques.save()
                else:
                    self.stdout.write("Proposition with no proof %s\n" % getText(prop.getElementsByTagName("statement")[0].childNodes))
            
            self.stdout.write('Successfully added questions for "%s"\n\n' % filename)
