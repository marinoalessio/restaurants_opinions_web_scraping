
let links = document.getElementsByTagName("a")
let len = links.length
for (var i = 0; i < len; i++) {
  links[i].onclick = function () {
    for (var j = 0; j < len; j++) {
      if (this == links[j]) {
        this.id = "actived"
      } else {
        links[j].id = ""
      }
    }
  }
}
