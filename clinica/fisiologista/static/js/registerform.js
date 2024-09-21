const input = document.querySelector('#CPF')

input.addEventListener('keypress', () => {
    let inputlength = input.value.length

    if (inputlength === 3 || inputlength === 7) {
        input.value += '.'
    } else if (inputlength === 11) {
        input.value += '-'
    }

})

const cell = document.querySelector('#telefone');

cell.addEventListener('input', function() {
    let value = cell.value.replace(/\D/g, '');

    if (value.length > 0) {
        if (value.length > 10) {
            cell.value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7, 11)}`;
        } else if (value.length > 6) {
            cell.value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6, 10)}`;
        } else if (value.length > 2) {
            cell.value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
        } else {
            cell.value = `(${value}`;
        }
    }
});

const text = document.querySelector('#CEP')

text.addEventListener('keypress', () => {
    let inputlength = text.value.length

    if (inputlength === 5) {
        text.value += '-'
    }
})

