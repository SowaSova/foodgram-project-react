import React from "react";

export function useTags() {
  const [ value, setValue ] = React.useState([])

  const handleChange = id => {
    console.log('handleChange id:', id)

    const valueUpdated = value.map(item => {
      console.log('item.id:', item.id, 'item.value:', item.value)
      if (item.id === id) {
        console.log('updating value')
        item.value = !item.value
      }
      return item
    })
    console.log('valueUpdated:', valueUpdated)
    setValue(valueUpdated)
  }

  return { value, handleChange, setValue }
}
