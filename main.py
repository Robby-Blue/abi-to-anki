import card_reader
import latex_writer
import genanki
import os

styling = """
.card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}
.media {
  maxwidth: 100%;
}
"""

data = card_reader.read_folder("subjects")
media_paths = latex_writer.create_latex(data)

deck = genanki.Deck(
  2010942553,
  "Abitur 2026")
package = genanki.Package(deck)

normal_model = genanki.Model(
  1958670534,
  "Normal Model",
  fields=[
    {"name": "Title"},
    {"name": "Solution"}
  ],
  templates=[
    {
      "name": "Card",
      "qfmt": "{{Title}}",
      "afmt": "{{FrontSide}}<hr id=\"answer\">{{Solution}}"
    },
  ],
  css=styling)

latex_model = genanki.Model(
  1515826472,
  "LaTex Media Model",
  fields=[
    {"name": "Title"},
    {"name": "Solution"},
    {"name": "LaTex"},
  ],
  templates=[
    {
      "name": "Card",
      "qfmt": "{{Title}} <br>\n\n<hr>\n{{LaTex}}",
      "afmt": "{{FrontSide}}<hr id=\"answer\">{{Solution}}",
    },
  ],
  css=styling)

for note in data:
  if "latex" in note:
    filename = note["guid"]+".answer.svg"
    image_path = f"<img src=\"{filename}\" class=\"media\">"
    anki_note = genanki.Note(
      model=latex_model,
      fields=[note["title"], note["solution"], image_path],
      guid=note["guid"])
  else:
    anki_note = genanki.Note(
      model=normal_model,
      fields=[note["title"], note["solution"]],
      guid=note["guid"])
  deck.add_note(anki_note)


package.media_files = media_paths

package.write_to_file("output.apkg")