__version__ = "v20191211"

bannerSheet = b"""%-12345X@PJL JOB
@PJL XCPT <?xml version="1.0" encoding="UTF-8"?>
@PJL XCPT <!DOCTYPE xpif SYSTEM "xpif-v02076.dtd">
@PJL XCPT <xpif version="1.0" cpss-version="2.07" xml:lang="en-US">
@PJL XCPT 	<job-template-attributes>
@PJL XCPT 		<adjust-lightness syntax="integer">0</adjust-lightness>
@PJL XCPT 		<color-effects-type syntax="keyword">monochrome-grayscale</color-effects-type>
@PJL XCPT 		<copies syntax="integer">1</copies>
@PJL XCPT 		<document-reading-orientation syntax="keyword">portrait</document-reading-orientation>
@PJL XCPT 		<finishings syntax="1setOf">
@PJL XCPT 			<value syntax="enum">3</value>
@PJL XCPT 		</finishings>
@PJL XCPT 		<halftone-graphics syntax="keyword">85-lpi</halftone-graphics>
@PJL XCPT 		<halftone-images syntax="keyword">85-lpi</halftone-images>
@PJL XCPT 		<halftone-text syntax="keyword">85-lpi</halftone-text>
@PJL XCPT 		<image-enhancement syntax="keyword">optimal-image-quality</image-enhancement>
@PJL XCPT 		<interleaved-sheets-col syntax="collection">
@PJL XCPT 			<interleaved-sheets-type syntax="keyword">none</interleaved-sheets-type>
@PJL XCPT 		</interleaved-sheets-col>
@PJL XCPT 		<job-offset syntax="1setOf">
@PJL XCPT 			<value syntax="keyword">offset-set</value>
@PJL XCPT 		</job-offset>
@PJL XCPT 		<job-save-disposition syntax="collection">
@PJL XCPT 			<save-disposition syntax="keyword">none</save-disposition>
@PJL XCPT 		</job-save-disposition>
@PJL XCPT 		<job-sheets syntax="keyword">none</job-sheets>
@PJL XCPT 		<client-default-attributes-col syntax="collection">
@PJL XCPT 			<media-col syntax="collection">
@PJL XCPT 				<input-tray syntax="keyword">automatic</input-tray>
@PJL XCPT 				<media-color syntax="keyword">white</media-color>
@PJL XCPT 				<media-type syntax="keyword">use-ready</media-type>
@PJL XCPT 			</media-col>
@PJL XCPT 			<print-quality-level syntax="keyword">high-speed</print-quality-level>
@PJL XCPT 			<sides syntax="keyword">one-sided</sides>
@PJL XCPT 		</client-default-attributes-col>
@PJL XCPT 		<output-bin syntax="keyword">stacker</output-bin>
@PJL XCPT 		<page-delivery syntax="keyword">same-order-face-down</page-delivery>
@PJL XCPT   <page-overrides syntax="1setOf">
@PJL XCPT 			<value syntax="collection">
@PJL XCPT 				<input-documents syntax="1setOf">
@PJL XCPT 					<value syntax="rangeOfInteger">
@PJL XCPT 						<lower-bound syntax="integer">1</lower-bound>
@PJL XCPT 						<upper-bound syntax="integer">1</upper-bound>
@PJL XCPT 					</value>
@PJL XCPT 				</input-documents>
@PJL XCPT 				<media-col syntax="collection">
@PJL XCPT 					<media-color syntax="keyword">other</media-color>
@PJL XCPT 				</media-col>
@PJL XCPT 				<pages syntax="1setOf">
@PJL XCPT 					<value syntax="rangeOfInteger">
@PJL XCPT 						<lower-bound syntax="integer">2</lower-bound>
@PJL XCPT 						<upper-bound syntax="integer">2</upper-bound>
@PJL XCPT 					</value>
@PJL XCPT 				</pages>
@PJL XCPT 			</value>
@PJL XCPT 		</page-overrides>
@PJL XCPT 		<pages-per-subset syntax="1setOf">
@PJL XCPT 			<value syntax="integer">0</value>
@PJL XCPT 		</pages-per-subset>
@PJL XCPT 		<pre-cut-tabs-image-shift syntax="integer">0</pre-cut-tabs-image-shift>
@PJL XCPT 		<separator-sheets syntax="collection">
@PJL XCPT 			<separator-sheets-type syntax="keyword">none</separator-sheets-type>
@PJL XCPT 		</separator-sheets>
@PJL XCPT 		<sheet-collate syntax="keyword">collated</sheet-collate>
@PJL XCPT 		<skip-blank-page syntax="keyword">none</skip-blank-page>
@PJL XCPT 		<toner-saver syntax="keyword">none</toner-saver>
@PJL XCPT 	</job-template-attributes>
@PJL XCPT 	<xpif-operation-attributes>
@PJL XCPT 		<creator-name-attributes syntax="keyword">windows-ps-driver</creator-name-attributes>
@PJL XCPT 		<creator-name-pdl syntax="name" xml:space="preserve">acrord32</creator-name-pdl>
@PJL XCPT 		<creator-version-attributes syntax="text" xml:space="preserve">5.303.15.0N 2013.03.15; DCP: GMAH(5.303.15.1)</creator-version-attributes>
@PJL XCPT 		<creator-version-pdl syntax="text" xml:space="preserve">19.12.20034.1161</creator-version-pdl>
@PJL XCPT 		<document-format syntax="mimeMediaType">application/postscript</document-format>
@PJL XCPT 		<host-address-col syntax="collection">
@PJL XCPT 			<host-address syntax="text" xml:space="preserve">172.16.132.128</host-address>
@PJL XCPT 			<host-address-type syntax="keyword">ipv4</host-address-type>
@PJL XCPT 		</host-address-col>
@PJL XCPT 		<job-id-from-client syntax="name" xml:space="preserve">Ticket</job-id-from-client>
@PJL XCPT 		<job-name syntax="name" xml:space="preserve">Ticket.pdf</job-name>
@PJL XCPT 		<job-originating-user-domain syntax="name" xml:space="preserve">Ticket</job-originating-user-domain>
@PJL XCPT 		<job-originating-user-name syntax="name" xml:space="preserve">Ticket</job-originating-user-name>
@PJL XCPT 		<requesting-user-name syntax="name" xml:space="preserve">Ticket</requesting-user-name>
@PJL XCPT 	</xpif-operation-attributes>
@PJL XCPT </xpif>
@PJL ENTER LANGUAGE = POSTSCRIPT"""
