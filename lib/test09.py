import xml_fragment_collector
import echo

print """Test XMLFragmentCollector"""
xfc = xml_fragment_collector.XMLFragmentCollector();
xfc.attach(echo.Echo())

print """basic test"""
xfc.update(xfc, "<a><b>")
xfc.update(xfc, "</b></a>")

print """should ignore trailing junk"""
xfc.update(xfc, "<a><b>")
xfc.update(xfc, "</b></a><")
xfc.update(xfc, "c>woof</c>")

