class SourceFile {
    constructor(name, binary_file) {
        this.name = name
        this.binary_file = binary_file
    }

    name = ""
    author = ""
    key_value ={}
    tags = []
    binary_file = null
}

export default SourceFile