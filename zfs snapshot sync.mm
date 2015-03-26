<map version="freeplane 1.3.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="zfs snapshot sync" ID="ID_1723255651" CREATED="1283093380553" MODIFIED="1427279913551"><hook NAME="MapStyle">

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node">
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right">
<stylenode LOCALIZED_TEXT="default" MAX_WIDTH="600" COLOR="#000000" STYLE="as_parent">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.note"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="5"/>
<node TEXT="get list of snapshots" POSITION="right" ID="ID_1733021543" CREATED="1427279915471" MODIFIED="1427279923413">
<edge COLOR="#ff0000"/>
<node TEXT="ssh to host1 and zfs list dataset -r -tsnapshot" ID="ID_84602630" CREATED="1427280265583" MODIFIED="1427280289660"/>
<node TEXT="ssh to host2 and zfs list dataset -r -tsnapshot" ID="ID_610706255" CREATED="1427280290287" MODIFIED="1427280308500"/>
<node TEXT="sort snapshots by dataset" ID="ID_155288798" CREATED="1427357680599" MODIFIED="1427357695469"/>
</node>
<node TEXT="compare list and see which one to send" POSITION="right" ID="ID_1895904436" CREATED="1427279925743" MODIFIED="1427279944549">
<edge COLOR="#0000ff"/>
<node TEXT="compile a set for each host" ID="ID_1294370998" CREATED="1427280312751" MODIFIED="1427280540076"/>
<node TEXT="transform path so it is comparable" ID="ID_569362055" CREATED="1427280540599" MODIFIED="1427280563155"/>
<node TEXT="actually compare set(host1) to set(host2) and keep differences" ID="ID_1661274910" CREATED="1427280563639" MODIFIED="1427280594532"/>
</node>
<node TEXT="actually send the snapshots" POSITION="right" ID="ID_532287043" CREATED="1427279945375" MODIFIED="1427279954613">
<edge COLOR="#00ff00"/>
<node TEXT="look at the differences list" ID="ID_732199426" CREATED="1427280605007" MODIFIED="1427280617252"/>
<node TEXT="send each snapshot from the first host to the other" ID="ID_66395715" CREATED="1427280617679" MODIFIED="1427280640660"/>
</node>
<node TEXT="verify that everything went well" POSITION="right" ID="ID_5157950" CREATED="1427279955215" MODIFIED="1427279977573">
<edge COLOR="#ff00ff"/>
<node TEXT="get a list of host2 snapshots" ID="ID_1306702280" CREATED="1427280643903" MODIFIED="1427280661349"/>
<node TEXT="compare new list to what was aimed" ID="ID_340241059" CREATED="1427280661999" MODIFIED="1427280756847"/>
<node TEXT="compute a resume of what happened" ID="ID_437437856" CREATED="1427280757495" MODIFIED="1427280773260">
<node TEXT="how many snapshots were transfered" ID="ID_72019753" CREATED="1427280774503" MODIFIED="1427280784916"/>
<node TEXT="how long did it take" ID="ID_1518142648" CREATED="1427280785231" MODIFIED="1427280791556"/>
<node TEXT="how much data does it represent" ID="ID_1280482875" CREATED="1427280792031" MODIFIED="1427280801605"/>
<node TEXT="how many space remains on host2" ID="ID_1020136001" CREATED="1427280803671" MODIFIED="1427280817084"/>
</node>
</node>
</node>
</map>
