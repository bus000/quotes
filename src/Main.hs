{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE OverloadedStrings #-}
module Main (main) where

import Data.Aeson (decode, FromJSON, ToJSON)
import Data.Aeson.Encode.Pretty (encodePretty)
import Data.Array (Array, array, (!), range)
import Data.ByteString.Char8 (unpack)
import qualified Data.ByteString.Lazy as B
import Data.Random () -- Import randomsource instance for IO.
import Data.Random.Extras (choice)
import Data.RVar (sampleRVar)
import GHC.Generics (Generic)
import Paths_quotes
import System.Console.CmdArgs
    ( help
    , explicit
    , (&=)
    , Data
    , Typeable
    , summary
    , helpArg
    , def
    , versionArg
    , name
    , cmdArgs
    )

data Quotes = Quotes
    { insertQuote :: Bool
    , quoteAuthor :: String
    , quote       :: String
    } deriving (Data, Typeable, Show, Eq)

quotes :: Quotes
quotes = Quotes
    { insertQuote = def &= help "Insert quote instead of printing"
    , quoteAuthor = def &= help "Author of the quote"
    , quote = def &= help "The actual quote"
    } &=
        help "Insert and get random quotes." &=
        summary "Quotes v0.1.0.0 (C) Magnus Stavngaard" &=
        helpArg [explicit, name "help", name "h"] &=
        versionArg [explicit, name "version", name "v"]

data Quote = Quote
    { content :: String
    , author  :: String
    } deriving (Generic, Show, Eq, Read)

instance FromJSON Quote
instance ToJSON Quote

main :: IO ()
main = do
    (Quotes shouldInsert auth cont) <- cmdArgs quotes

    quoteFileName <- getDataFileName "./data/quotes.json"
    quotesMay <- fmap decode $ B.readFile quoteFileName

    case quotesMay of
        Just quotes -> if shouldInsert
            then insertTheQuote quotes quoteFileName auth cont
            else showQuote quotes
        Nothing -> putStrLn "Could not load quotes"

showQuote :: [Quote] -> IO ()
showQuote qs = do
    q <- sampleRVar $ choice qs
    putStrLn $ quoteToStr q

insertTheQuote :: [Quote] -> FilePath -> String -> String -> IO ()
insertTheQuote qs f auth cont = case duplicates of
    [] -> B.writeFile f $ encodePretty ((Quote cont auth):qs)
    (dcont:_) -> putStrLn $ concat
        ["The quote \"", dcont, "\" is very similar. Not inserting."]
  where
    duplicates = filter (\c -> editDistance c cont < 10) contents
    contents = map content qs

quoteToStr :: Quote -> String
quoteToStr (Quote cont auth) = cont ++ "\n    - " ++ auth

{- Function taken from https://wiki.haskell.org/Edit_distance. -}
editDistance :: Eq a => [a] -> [a] -> Int
editDistance xs ys = table ! (m,n)
  where
    (m,n) = (length xs, length ys)
    x     = array (1,m) (zip [1..] xs)
    y     = array (1,n) (zip [1..] ys)

    table :: Array (Int,Int) Int
    table = array bnds [(ij, dist ij) | ij <- range bnds]
    bnds  = ((0,0),(m,n))

    dist (0,j) = j
    dist (i,0) = i
    dist (i,j) = minimum [table ! (i-1,j) + 1, table ! (i,j-1) + 1,
        if x ! i == y ! j then table ! (i-1,j-1) else 1 + table ! (i-1,j-1)]
