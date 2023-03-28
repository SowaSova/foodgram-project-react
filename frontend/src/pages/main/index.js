import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const HomePage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    tagsValue,
    setTagsValue: setValue,
    handleTagsChange,
    handleLike,
    handleAddToCart
  } = useRecipes()

  console.log('HomePage tagsValue:', tagsValue)


  const getRecipes = ({ page = 1, tags }) => {
    api
      .getRecipes({ page, tags })
      .then(res => {
        const { results, count } = res
        setRecipes(results)
        setRecipesCount(count)
      })
  }

  useEffect(_ => {
    console.log('tagsValue:', tagsValue)
    getRecipes({ page: recipesPage, tags: tagsValue })
  }, [recipesPage, tagsValue])

  useEffect(_ => {
    api.getTags()
      .then(data => {
        if (data && Array.isArray(data.results)) {
          setValue(data.results.map(tag => ({ ...tag, value: true })))
        } else {
          console.error('Ошибка: data.results не является массивом', data)
        }
      })
  }, [])

  return <Main>
    <Container>
      <MetaTags>
        <title>Рецепты</title>
        <meta name="description" content="Продуктовый помощник - Рецепты" />
        <meta property="og:title" content="Рецепты" />
      </MetaTags>
      <div className={styles.title}>
        <Title title='Рецепты' />
        <CheckboxGroup
          values={tagsValue}
          handleChange={value => {
            setRecipesPage(1)
            handleTagsChange(value)
          }}
        />
      </div>
      <CardList>
        {recipes.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <Pagination
        count={recipesCount}
        limit={6}
        page={recipesPage}
        onPageChange={page => setRecipesPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

